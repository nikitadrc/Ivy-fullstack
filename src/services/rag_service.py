from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import DirectoryLoader, TextLoader
from typing import List, Dict, Any, Optional
import os
from models import RoleType, QuestionType

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.llm = ChatOpenAI(temperature=0.7)
        self.vector_stores = {}
        self.initialize_vector_stores()

    def initialize_vector_stores(self):
        """Initialize vector stores for different roles and question types"""
        roles_data = {
            RoleType.FRONTEND: "data/frontend",
            RoleType.BACKEND: "data/backend",
            RoleType.FULLSTACK: "data/fullstack",
            RoleType.DATA_SCIENTIST: "data/data_science",
            RoleType.DEVOPS: "data/devops",
            RoleType.AI_ML: "data/ai_ml",
            RoleType.QA: "data/qa"
        }
        
        for role, data_path in roles_data.items():
            if os.path.exists(data_path):
                documents = DirectoryLoader(data_path).load()
                texts = self.text_splitter.split_documents(documents)
                self.vector_stores[role] = FAISS.from_documents(texts, self.embeddings)

    def get_chat_chain(self, role: RoleType, memory: Optional[ConversationBufferMemory] = None) -> ConversationalRetrievalChain:
        """Create a conversational chain for the specified role"""
        if memory is None:
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        vector_store = self.vector_stores.get(role)
        if not vector_store:
            raise ValueError(f"No vector store found for role: {role}")
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.as_retriever(),
            memory=memory,
            return_source_documents=True
        )

    def process_question(
        self,
        question: str,
        role: RoleType,
        question_type: QuestionType,
        chat_history: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a question and return an answer with context"""
        # Convert chat history to the format expected by LangChain
        formatted_history = []
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    formatted_history.append(("human", msg["content"]))
                else:
                    formatted_history.append(("assistant", msg["content"]))

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=formatted_history
        )

        chain = self.get_chat_chain(role, memory)
        
        # Prepare the prompt based on question type
        prompt = self._prepare_prompt(question, question_type)
        
        # Get the response
        response = chain({"question": prompt})
        
        # Extract relevant information
        answer = response["answer"]
        source_documents = response["source_documents"]
        
        # Get context references
        context_used = [doc.metadata.get("source", "") for doc in source_documents]
        
        return {
            "answer": answer,
            "context_used": context_used,
            "confidence_score": self._calculate_confidence(response),
            "suggested_topics": self._suggest_related_topics(question, role, source_documents)
        }

    def _prepare_prompt(self, question: str, question_type: QuestionType) -> str:
        """Prepare the prompt based on question type"""
        prompts = {
            QuestionType.TECHNICAL: f"Explain the technical concept: {question}",
            QuestionType.CODING: f"Here's a coding problem to solve: {question}",
            QuestionType.BEHAVIORAL: f"Here's a behavioral question: {question}",
            QuestionType.SYSTEM_DESIGN: f"Design a system for: {question}",
            QuestionType.RESUME: f"Regarding the resume: {question}"
        }
        return prompts.get(question_type, question)

    def _calculate_confidence(self, response: Dict[str, Any]) -> float:
        """Calculate confidence score based on response"""
        # Implement confidence calculation logic
        # This is a placeholder implementation
        return 0.85

    def _suggest_related_topics(
        self,
        question: str,
        role: RoleType,
        source_documents: List[Any]
    ) -> List[str]:
        """Suggest related topics based on the question and context"""
        # Implement topic suggestion logic
        # This is a placeholder implementation
        return ["Data Structures", "Algorithms", "System Design Patterns"] 