AI Interview Chatbot
A modular, full-stack AI-powered chatbot for automated candidate screening, interview Q&A, answer evaluation, feedback, analytics, and more—built with Python, Streamlit, LangChain, and state-of-the-art NLP models.

Table of Contents
Introduction

Key Features

Project Structure

Installation

Usage

Configuration & Environment Variables

Sample Data

Testing

Contributing

License

Contact

Introduction
This project is an AI Interview Chatbot designed to automate the initial stages of candidate screening and interviews. It leverages Retrieval-Augmented Generation (RAG), semantic answer evaluation, sentiment analysis, and a user-friendly web interface to streamline the recruitment process for HR teams and enhance candidate experience.

Key Features
Automated Candidate Screening: Multi-category (Technical, Behavioral, HR) question flow.

Semantic Answer Evaluation: Scores and provides feedback using sentence embeddings.

Sentiment Analysis: Detects candidate attitude and confidence.

FAQ Handling: Static and AI-generated answers to candidate questions.

Human Handoff: Escalates to a recruiter when needed.

Analytics Dashboard: Real-time recruiter insights and process bottlenecks.

Modular Frontend & Backend: Built with Streamlit and Python for rapid prototyping and extension.

Easy Data Integration: Uses JSON files for question banks and model answers.

Project Structure
text
your_project/
├── data/                      # JSON question banks, logs, and sample responses
│   ├── technical_questions.json
│   ├── behavioral_questions.json
│   ├── hr_questions.json
│   └── interaction_logs.csv
├── frontend/
│   ├── app.py                 # Main Streamlit app
│   └── components/            # UI components (header, form, question, feedback, etc.)
├── src/
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── sentiment_analysis.py
│   ├── human_handoff.py
│   ├── faq_module.py
│   ├── rag_pipeline.py
│   ├── analytics.py
│   └── utils.py
├── tests/                     # Unit and integration tests
│   ├── test_chatbot.py
│   ├── test_data_loader.py
│   ├── test_rag_pipeline.py
├── requirements.txt
├── .env
├── README.md
└── Dockerfile