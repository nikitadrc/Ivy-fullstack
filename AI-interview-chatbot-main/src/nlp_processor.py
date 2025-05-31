# src/nlp_processor.py

import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    """Cache the Hugging Face model to avoid reloading on every interaction"""
    return pipeline(
        "text2text-generation", 
        model="google/flan-t5-base",
        device_map="auto"  # Automatically uses GPU if available
    )

def nlp_response_fn(question: str) -> str:
    """
    Generate an AI answer to a user question using a local Hugging Face model.
    Uses Streamlit's caching for efficient model loading.
    """
    pipe = load_model()
    prompt = f"Answer this interview-related question concisely: {question}"
    response = pipe(
        prompt,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True,
        truncation=True
    )
    return response[0]['generated_text'].strip()

# Example usage
if __name__ == "__main__":
    print(nlp_response_fn("What is the interview process at this company?"))
