# src/rag_pipeline.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os
import json

# 1. Indexing Phase: Ingest, Chunk, Embed, Store

def build_vector_store_from_json(
    json_paths,
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
    chunk_size=500,
    chunk_overlap=50
):
    """
    Load questions and model answers from JSON files, chunk, embed, and store in FAISS vector DB.
    Returns the FAISS vector store object.
    """
    # Load all questions and answers
    docs = []
    for path in json_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                q = item.get("question", "")
                a = item.get("model_answer", "")
                category = os.path.splitext(os.path.basename(path))[0].replace("_questions", "")
                text = f"Category: {category}\nQuestion: {q}\nAnswer: {a}"
                docs.append(text)
    
    # Chunking (split long docs if needed)
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))
    
    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    # Build FAISS vector store
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

# 2. Retrieval and Generation Phase

def get_rag_chain(vector_store, openai_api_key=None, llm_temperature=0.2):
    """
    Create a RetrievalQA chain using the vector store and an LLM.
    """
    # Use OpenAI LLM (or swap for HuggingFacePipeline if preferred)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=llm_temperature)
    retriever = vector_store.as_retriever()
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return rag_chain

def answer_query(rag_chain, query):
    """
    Use the RAG chain to answer a user query.
    Returns the answer and source documents.
    """
    result = rag_chain(query)
    answer = result['result']
    sources = result.get('source_documents', [])
    return answer, sources

# Example usage (for testing/demo)
if __name__ == "__main__":
    # Paths to your JSON files
    json_paths = [
        "data/technical_questions.json",
        "data/behavioral_questions.json",
        "data/hr_questions.json"
    ]
    # Build vector store
    vector_store = build_vector_store_from_json(json_paths)
    
    # You need your OpenAI API key (set as env variable or pass directly)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    rag_chain = get_rag_chain(vector_store, openai_api_key=openai_api_key)
    
    # Example query
    query = "What is object-oriented programming?"
    answer, sources = answer_query(rag_chain, query)
    print("Answer:", answer)
    print("Sources:", sources)
