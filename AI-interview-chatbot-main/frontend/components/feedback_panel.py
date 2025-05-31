# frontend/components/feedback_panel.py

import streamlit as st

def show_feedback(feedback_text=None, strengths=None, improvements=None, score=None, sentiment=None, show_header=True):
    """
    Display feedback to the candidate.

    Args:
        feedback_text (str): General feedback message.
        strengths (list): List of strengths identified in the answer.
        improvements (list): List of suggested improvements.
        score (float or int): Numeric score for the answer.
        sentiment (str): Sentiment analysis result (e.g., "Positive", "Neutral", "Negative").
        show_header (bool): Whether to display the "Feedback" header.
    """
    if show_header:
        st.subheader("📝 Feedback")

    if feedback_text:
        st.info(feedback_text)

    if score is not None:
        st.markdown(f"**Score:** `{score}`")

    if sentiment:
        st.markdown(f"**Sentiment:** `{sentiment}`")

    if strengths:
        st.markdown("**Strengths:**")
        for s in strengths:
            st.success(f"✔️ {s}")

    if improvements:
        st.markdown("**Suggestions for Improvement:**")
        for i in improvements:
            st.warning(f"➖ {i}")

    if not any([feedback_text, strengths, improvements, score, sentiment]):
        st.info("No feedback available yet.")

# Example usage (for testing/demo)
if __name__ == "__main__":
    st.set_page_config(page_title="Feedback Panel Demo")
    st.title("Feedback Panel Demo")

    show_feedback(
        feedback_text="Great explanation of object-oriented principles!",
        strengths=["Clear structure", "Good use of examples"],
        improvements=["Could mention SOLID principles", "Expand on inheritance"],
        score=4.5,
        sentiment="Positive"
    )
