# src/faq_module.py

from typing import Dict, Callable, Optional

def get_static_faq_answer(user_question: str, static_faqs: Dict[str, str]) -> Optional[str]:
    """
    Try to match the user's question to a static FAQ using simple keyword search.

    Args:
        user_question (str): The question asked by the user.
        static_faqs (dict): Dictionary of {question: answer} pairs.

    Returns:
        str: The matched answer, or None if no match is found.
    """
    user_q_lower = user_question.lower()
    for faq_q, faq_a in static_faqs.items():
        if user_q_lower in faq_q.lower() or faq_q.lower() in user_q_lower:
            return faq_a
    return None

def get_faq_answer(
    user_question: str,
    static_faqs: Dict[str, str],
    nlp_response_fn: Optional[Callable[[str], str]] = None
) -> str:
    """
    Get an answer to the user's FAQ. Tries static match first, then uses AI if available.

    Args:
        user_question (str): The question asked by the user.
        static_faqs (dict): Dictionary of {question: answer} pairs.
        nlp_response_fn (callable, optional): Function to generate AI answer.

    Returns:
        str: The answer to display.
    """
    # First try static FAQ match
    static_answer = get_static_faq_answer(user_question, static_faqs)
    if static_answer:
        return static_answer

    # If no static match and AI is available, use it
    if nlp_response_fn:
        try:
            ai_answer = nlp_response_fn(user_question)
            return ai_answer
        except Exception as e:
            return f"Sorry, I couldn't generate an answer due to an error: {e}"

    # Fallback if nothing found
    return "Sorry, I couldn't find an answer to your question. Please contact support or try rephrasing your question."

# Example usage (for testing/demo)
if __name__ == "__main__":
    example_faqs = {
        "What is the interview process?": "Our process includes an initial screening, technical round, and HR round.",
        "How long does the interview take?": "The automated interview typically takes 20-30 minutes.",
        "Can I retake the interview?": "Currently, retakes are not allowed unless invited by HR.",
        "Who can I contact for support?": "Please email hr@example.com for any support queries."
    }

    # Dummy AI function for testing
    def dummy_nlp_response(q):
        return f"(AI) Sorry, I don't have a static answer for: {q}"

    print(get_faq_answer("What is the interview process?", example_faqs))
    print(get_faq_answer("Tell me about the process", example_faqs, dummy_nlp_response))
    print(get_faq_answer("Is there a dress code?", example_faqs, dummy_nlp_response))
