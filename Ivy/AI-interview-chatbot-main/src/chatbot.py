# src/chatbot.py

from src.evaluation import evaluate_answer
from src.sentiment_analysis import analyze_sentiment
from src.human_handoff import handle_human_handoff
from src.analytics import log_interaction  # Optional: for analytics logging
import streamlit as st
from datetime import datetime

def run_chatbot(
    questions,
    candidate_data,
    current_index,
    scores,
    conversation_history,
    on_complete
):
    """
    Orchestrates the chatbot interview flow.

    Args:
        questions (list): List of dicts with keys: 'text', 'category', 'model_answer'
        candidate_data (dict): Candidate info
        current_index (int): Current question index
        scores (list): List of previous scores
        conversation_history (list): List of dicts with Q&A and metadata
        on_complete (callable): Function to call when interview is complete
    """
    # If all questions answered, finish interview
    if current_index >= len(questions):
        on_complete(scores, conversation_history)
        return

    question = questions[current_index]
    st.markdown(f"**Category:** `{question['category']}`")
    st.markdown(f"**Question {current_index+1} of {len(questions)}**")
    st.markdown(f"### {question['text']}")

    # Get candidate answer
    answer = st.text_area(
        "Your Answer:",
        key=f"answer_{current_index}"
    )
    submitted = st.button("Submit Answer", key=f"submit_{current_index}")

    if submitted and answer.strip():
        # Evaluate answer
        score, feedback = evaluate_answer(answer, question['model_answer'])
        sentiment_result = analyze_sentiment(answer)
        sentiment = sentiment_result['label']

        # Human handoff check
        handoff_triggered = handle_human_handoff(
            candidate_response=answer,
            sentiment=sentiment,
            context={
                **candidate_data,
                "question": question['text'],
                "answer": answer,
                "score": score,
                "sentiment": sentiment
            }
        )
        if handoff_triggered:
            st.stop()

        # Show feedback
        st.success(f"Score: {score}/5")
        st.info(f"Feedback: {feedback}")
        st.info(f"Sentiment: {sentiment}")

        # Log interaction (optional)
        if 'candidate_id' in candidate_data:
            log_interaction(
                candidate_id=candidate_data['candidate_id'],
                question_type=question['category'],
                question=question['text'],
                answer=answer,
                score=score,
                feedback=feedback,
                sentiment=sentiment,
                duration=0  # You can add timing logic if desired
            )

        # Update state
        scores.append(score)
        conversation_history.append({
            "question": question['text'],
            "category": question['category'],
            "model_answer": question['model_answer'],
            "candidate_answer": answer,
            "score": score,
            "feedback": feedback,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()
        })

        # Move to next question
        st.session_state['interview_state']['current_question_index'] += 1
        st.experimental_rerun()

    elif submitted:
        st.warning("Please enter your answer before submitting.")

