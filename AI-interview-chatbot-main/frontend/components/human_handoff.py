# src/human_handoff.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os

HANDOFF_LOG_PATH = "data/handoff_requests.csv"

def detect_handoff_need(candidate_response: str, sentiment: str = None) -> bool:
    """
    Determine if conversation should be transferred to a human.

    Args:
        candidate_response: Candidate's latest message
        sentiment: Optional sentiment analysis result

    Returns:
        bool: True if handoff should be initiated
    """
    manual_triggers = ["human", "representative", "talk to someone", "recruiter", "real person", "manager"]
    if candidate_response and any(keyword in candidate_response.lower() for keyword in manual_triggers):
        return True
    if sentiment and sentiment.lower() in ["negative", "frustrated"]:
        return True
    return False

def log_handoff_request(reason: str, context: dict):
    """
    Log handoff request to CSV for recruiter follow-up.

    Args:
        reason: Reason for handoff (e.g., "candidate request", "negative sentiment")
        context: Candidate data and conversation context
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "candidate_id": context.get("candidate_id", ""),
        "name": context.get("name", ""),
        "email": context.get("email", ""),
        "reason": reason,
        "last_message": context.get("last_message", ""),
        "sentiment": context.get("sentiment", ""),
        "status": "pending"
    }

    # Ensure directory exists
    os.makedirs(os.path.dirname(HANDOFF_LOG_PATH), exist_ok=True)

    # Append to CSV (create if not exists)
    try:
        file_exists = os.path.isfile(HANDOFF_LOG_PATH)
        df = pd.DataFrame([log_entry])
        df.to_csv(HANDOFF_LOG_PATH, mode='a', header=not file_exists, index=False)
    except Exception as e:
        st.error(f"Error logging handoff request: {str(e)}")

def handoff_interface(context: dict):
    """
    Display handoff UI and handle transition.

    Args:
        context: Current conversation context and candidate data
    """
    st.session_state['handoff_requested'] = True

    with st.sidebar:
        st.error("⚠️ Human Handoff Requested")
        st.write(f"**Candidate:** {context.get('name', '')}")
        st.write(f"**Reason:** {context.get('handoff_reason', '')}")
        st.write(f"**Last Message:** {context.get('last_message', '')}")

    st.title("👥 Human Assistance Requested")
    st.success("""
    A recruiter will contact you shortly.  
    **Here's what happens next:**
    1. We've notified our HR team.
    2. You'll receive an email within 24 hours.
    3. Please check your inbox for further instructions.
    """)

    # Optional: Collect additional info
    with st.expander("Provide Additional Comments"):
        comments = st.text_area("Any additional information for the recruiter?")
        if st.button("Submit Comments"):
            context['comments'] = comments
            log_handoff_request(context['handoff_reason'], context)
            st.success("Comments submitted successfully!")

def handle_human_handoff(candidate_response: str, sentiment: str, context: dict):
    """
    Main handoff handler to be called from chatbot flow.

    Args:
        candidate_response: Candidate's latest message
        sentiment: Sentiment analysis result
        context: Conversation context

    Returns:
        bool: True if handoff was triggered and UI was shown.
    """
    # Only trigger once per session
    if st.session_state.get('handoff_requested', False):
        handoff_interface(context)
        return True

    handoff_needed = detect_handoff_need(candidate_response, sentiment)
    if handoff_needed:
        reason = ("Candidate request"
                  if candidate_response and any(keyword in candidate_response.lower()
                                               for keyword in ["human", "representative", "recruiter", "real person"])
                  else f"Automated trigger: {sentiment} sentiment")

        context = context.copy() if context else {}
        context.update({
            "handoff_reason": reason,
            "last_message": candidate_response,
            "sentiment": sentiment
        })

        log_handoff_request(reason, context)
        handoff_interface(context)
        return True

    return False

# Example usage (for testing/demo)
if __name__ == "__main__":
    st.set_page_config(page_title="Handoff Demo")

    mock_context = {
        "candidate_id": "123",
        "name": "John Doe",
        "email": "john@example.com"
    }

    if not st.session_state.get('handoff_requested'):
        user_input = st.text_input("Test handoff (try: 'I want to talk to a human')")
        if user_input:
            if handle_human_handoff(user_input, "neutral", mock_context):
                st.stop()
    else:
        handoff_interface(mock_context)

