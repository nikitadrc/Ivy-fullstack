# frontend/app.py
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import json
import os
import sys
from datetime import datetime
from src.sentiment_analysis import analyze_sentiment
from src.human_handoff import handle_human_handoff
from src.evaluation import evaluate_answer
from src.data_loader import load_questions

# Add components directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'components')))
from components.header import show_header
from components.candidate_form import candidate_form
from components.question_display import display_question
from components.feedback_panel import show_feedback
from components.faq_section import show_faq_section
from components.status_update import show_status_update
from components.analytics_dashboard import show_analytics_dashboard

# --- Session State Initialization ---
if 'interview_state' not in st.session_state:
    st.session_state['interview_state'] = {
        'current_stage': 'form',
        'current_question_index': 0,
        'scores': [],
        'start_time': None,
        'candidate_data': None,
        'conversation_history': []
    }

def main():
    st.set_page_config(
        page_title="AI Interview Bot",
        page_icon="🤖",
        layout="centered"
    )

    # Navigation
    page = st.sidebar.selectbox("Navigation", ["Candidate Interview", "Recruiter Dashboard"])

    if page == "Recruiter Dashboard":
        show_analytics_dashboard()
        return

    show_header()
    questions = load_questions()

    # Stage 1: Candidate Form
    if st.session_state['interview_state']['current_stage'] == 'form':
        candidate_form()
        if 'candidate_data' in st.session_state and st.session_state['candidate_data']:
            st.session_state['interview_state']['candidate_data'] = st.session_state['candidate_data']
            st.session_state['interview_state']['current_stage'] = 'interview'
            st.session_state['interview_state']['start_time'] = datetime.now()
            st.experimental_rerun()

    # Stage 2: Interview Questions
    elif st.session_state['interview_state']['current_stage'] == 'interview':
        handle_interview_flow(questions)

    # Stage 3: Final Feedback
    else:
        show_final_feedback()

def handle_interview_flow(questions):
    current_index = st.session_state['interview_state']['current_question_index']
    conversation_history = st.session_state['interview_state']['conversation_history']

    if current_index < len(questions):
        question = questions[current_index]

        answer, submitted = display_question(
            question_text=question['text'],
            question_number=current_index + 1,
            total_questions=len(questions),
            question_category=question['category']
        )

        if submitted:
            # Evaluate answer
            score, feedback = evaluate_answer(
                answer=answer,
                model_answer=question['model_answer']
            )

            # Sentiment analysis
            sentiment_result = analyze_sentiment(answer)
            sentiment = sentiment_result['label']

            # Human handoff check
            handoff_triggered = handle_human_handoff(
                candidate_response=answer,
                sentiment=sentiment,
                context=st.session_state['interview_state']['candidate_data']
            )
            if handoff_triggered:
                st.stop()

            # Store results
            st.session_state['interview_state']['scores'].append(score)
            st.session_state['interview_state']['conversation_history'].append({
                "question": question['text'],
                "category": question['category'],
                "model_answer": question['model_answer'],
                "candidate_answer": answer,
                "score": score,
                "feedback": feedback,
                "sentiment": sentiment,
                "timestamp": datetime.now().isoformat()
            })

            # Show feedback
            show_feedback(
                feedback_text=feedback,
                score=score,
                sentiment=sentiment,
                show_header=False
            )

            # Move to next question
            st.session_state['interview_state']['current_question_index'] += 1
            st.experimental_rerun()

        # FAQ Section (always available)
        show_faq_section(static_faqs=get_static_faqs())

    else:
        st.session_state['interview_state']['current_stage'] = 'complete'
        st.experimental_rerun()

def show_final_feedback():
    scores = st.session_state['interview_state']['scores']
    total_score = sum(scores)
    avg_score = total_score / len(scores) if scores else 0

    show_status_update(
        message=f"Interview Complete! Average Score: {avg_score:.1f}/5",
        status_type="success"
    )

    st.subheader("Final Feedback")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Questions", len(scores))
        st.metric("Total Score", f"{total_score}/{(len(scores) * 5)}")

    with col2:
        st.metric("Average Score", f"{avg_score:.1f}/5")
        duration = 0
        if st.session_state['interview_state']['start_time']:
            duration = (datetime.now() - st.session_state['interview_state']['start_time']).seconds // 60
        st.metric("Duration", f"{duration} minutes")

    if avg_score >= 3.5:
        show_status_update(
            message="Congratulations! You've been shortlisted for the next round.",
            status_type="success"
        )
    else:
        show_status_update(
            message="Thank you for your time. We'll be in touch if there are updates.",
            status_type="info"
        )

    # Optionally, show conversation history for review
    with st.expander("View Your Interview Transcript"):
        for entry in st.session_state['interview_state']['conversation_history']:
            st.markdown(f"**Q:** {entry['question']}")
            st.markdown(f"**Your Answer:** {entry['candidate_answer']}")
            st.markdown(f"**Score:** {entry['score']}  |  **Feedback:** {entry['feedback']}  |  **Sentiment:** {entry['sentiment']}")
            st.markdown("---")

def get_static_faqs():
    return {
        "What happens after the interview?": "Our HR team will review your results and contact you within 3 business days.",
        "Can I review my answers?": "Yes, you'll receive a copy of your interview transcript via email.",
        "How is my score calculated?": "Scores are based on answer relevance, depth, and comparison with model answers."
    }

if __name__ == "__main__":
    main()
