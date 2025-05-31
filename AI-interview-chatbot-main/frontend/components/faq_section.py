# frontend/components/faq_section.py

import streamlit as st

def show_faq_section(static_faqs=None, nlp_response_fn=None):
    """
    Display FAQ section in the sidebar.
    
    Args:
        static_faqs (dict): A dictionary of {question: answer} for standard FAQs.
        nlp_response_fn (callable): Optional. A function that takes a user question (str) and returns an answer (str)
                                    for dynamic/NLP-powered FAQ responses.
    """
    st.sidebar.header("❓ Frequently Asked Questions")
    
    if static_faqs:
        st.sidebar.subheader("Browse FAQs")
        for idx, (question, answer) in enumerate(static_faqs.items()):
            with st.sidebar.expander(f"Q{idx+1}: {question}"):
                st.write(answer)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Ask Your Own Question")
    user_question = st.sidebar.text_input("Type your question about the process, company, or role:")

    if user_question:
        if nlp_response_fn:
            try:
                answer = nlp_response_fn(user_question)
                st.sidebar.info(f"**AI Answer:** {answer}")
            except Exception as e:
                st.sidebar.error(f"Error generating answer: {e}")
        elif static_faqs:
            # Try to match with static FAQs (simple keyword search)
            matched = False
            for q, a in static_faqs.items():
                if user_question.lower() in q.lower():
                    st.sidebar.info(f"**FAQ Match:** {a}")
                    matched = True
                    break
            if not matched:
                st.sidebar.warning("Sorry, I couldn't find an answer. Please contact support or try rephrasing your question.")
        else:
            st.sidebar.warning("No FAQ data available.")

# Example usage (for testing/demo)
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
    from nlp_processor import nlp_response_fn  # Make sure this exists!

    # Example static FAQs
    example_faqs = {
        "What is the interview process?": "Our process includes an initial screening, technical round, and HR round.",
        "How long does the interview take?": "The automated interview typically takes 20-30 minutes.",
        "Can I retake the interview?": "Currently, retakes are not allowed unless invited by HR.",
        "Who can I contact for support?": "Please email hr@example.com for any support queries."
    }

    st.set_page_config(page_title="FAQ Section Demo")
    st.title("FAQ Section Demo")
    show_faq_section(static_faqs=example_faqs, nlp_response_fn=nlp_response_fn)
