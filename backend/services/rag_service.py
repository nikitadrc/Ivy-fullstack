from typing import List, Optional, Dict
import os
import json
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGService:
    def __init__(self):
        self.llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = None
        self.questions = self.load_questions()
        self.evaluation_criteria = self.load_evaluation_criteria()
        self.sample_responses = self.load_sample_responses()
        self.initialize_vector_store()

    def load_questions(self) -> Dict:
        questions = {
            'technical': [],
            'behavioral': [],
            'hr': []
        }
        
        # Load technical questions
        tech_path = os.path.join('AI-interview-chatbot-main', 'data', 'technical_questions.json')
        with open(tech_path, 'r') as f:
            tech_data = json.load(f)
            questions['technical'] = tech_data['questions']

        # Load behavioral questions
        behav_path = os.path.join('AI-interview-chatbot-main', 'data', 'behavioral_questions.json')
        with open(behav_path, 'r') as f:
            behav_data = json.load(f)
            questions['behavioral'] = behav_data['behavioral_questions']

        # Load HR questions
        hr_path = os.path.join('AI-interview-chatbot-main', 'data', 'hr_questions.json')
        with open(hr_path, 'r') as f:
            questions['hr'] = json.load(f)

        return questions

    def load_evaluation_criteria(self) -> Dict:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'evaluation_criteria.json'), 'r') as f:
            return json.load(f)

    def load_sample_responses(self) -> Dict:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_responses.json'), 'r') as f:
            return json.load(f)

    def initialize_vector_store(self):
        # Convert questions and responses into documents for the vector store
        documents = []
        
        # Process all question types
        for q_type, questions in self.questions.items():
            for q in questions:
                doc = {
                    "content": f"Question Type: {q_type}\nQuestion: {q['question']}\nAnswer: {q['answer']}\nDifficulty: {q['difficulty']}\nFeedback: {q['feedback']}",
                    "metadata": {
                        "id": q['candidate_id'],
                        "type": q_type,
                        "difficulty": q['difficulty'],
                        "score": q['score']
                    }
                }
                documents.append(doc)
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Split documents
        texts = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)

    def get_response(self, question: str, role: str, question_type: str) -> Dict:
        # Create retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
        
        # Get response
        context = f"You are an AI interview assistant helping a {role} developer with a {question_type} question."
        query = f"Context: {context}\nQuestion: {question}\nProvide a detailed answer with examples if applicable."
        
        response = qa_chain.run(query)
        
        # Get relevant documents for context
        docs = self.vector_store.similarity_search(question, k=3)
        context_used = [doc.page_content for doc in docs]
        
        # Calculate confidence score based on similarity to existing questions
        confidence_score = self.calculate_confidence_score(question, docs)
        
        # Get suggested topics based on the role and question type
        suggested_topics = self.get_suggested_topics(question, role, question_type)
        
        return {
            "answer": response,
            "context_used": context_used,
            "confidence_score": confidence_score,
            "suggested_topics": suggested_topics
        }

    def calculate_confidence_score(self, question: str, similar_docs: List) -> float:
        # Calculate confidence based on similarity scores of retrieved documents
        if not similar_docs:
            return 0.5
        
        # Get the average score of similar questions
        scores = [doc.metadata.get('score', 0) for doc in similar_docs if 'score' in doc.metadata]
        return sum(scores) / len(scores) if scores else 0.7

    def get_suggested_topics(self, question: str, role: str, question_type: str) -> List[str]:
        # Get similar questions and extract their topics
        similar_docs = self.vector_store.similarity_search(question, k=5)
        topics = set()
        
        for doc in similar_docs:
            # Extract topics from the content
            content = doc.page_content.lower()
            if 'react' in content:
                topics.add('React')
            if 'javascript' in content:
                topics.add('JavaScript')
            if 'python' in content:
                topics.add('Python')
            if 'database' in content or 'sql' in content:
                topics.add('Databases')
            if 'algorithm' in content:
                topics.add('Algorithms')
            if 'system design' in content:
                topics.add('System Design')
            if 'machine learning' in content or 'ai' in content:
                topics.add('Machine Learning')
            
        return list(topics) 