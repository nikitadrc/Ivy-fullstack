# frontend/components/question_display.py

import streamlit as st

def display_question(
    question_text,
    question_number=None,
    total_questions=None,
    question_category=None,
    previous_answer=None,
    disable_input=False,
    submit_label="Submit Answer"
):
    """
    Display the current interview question and collect the candidate's answer.

    Args:
        question_text (str): The question to display.
        question_number (int, optional): Current question number.
        total_questions (int, optional): Total number of questions.
        question_category (str, optional): Category (e.g., "Technical", "Behavioral", "HR").
        previous_answer (str, optional): Pre-fill answer if available.
        disable_input (bool): If True, disables the answer input.
        submit_label (str): Label for the submit button.

    Returns:
        (answer, submitted): Tuple of the candidate's answer and submit status.
    """
    # Display question metadata
    if question_category:
        st.markdown(f"**Category:** `{question_category}`")
    if question_number and total_questions:
        st.markdown(f"**Question {question_number} of {total_questions}**")
    
    # Display the question
    st.markdown(f"### {question_text}")
    
    # Answer input
    answer = st.text_area(
        "Your Answer:",
        value=previous_answer or "",
        disabled=disable_input,
        key=f"answer_{question_number or question_text[:10]}"
    )
    
    # Submit button
    submitted = st.button(submit_label, disabled=disable_input, key=f"submit_{question_number or question_text[:10]}")
    
    return answer, submitted

# Example usage (for testing/demo)
if __name__ == "__main__":
    st.set_page_config(page_title="Question Display Demo")
    st.title("Question Display Demo")
    
    question = "Can you explain the concept of object-oriented programming?"
    category = "Technical"
    q_num = 1
    total_qs = 10
    
    answer, submitted = display_question(
        question_text=question,
        question_number=q_num,
        total_questions=total_qs,
        question_category=category
    )
    
    if submitted:
        st.success(f"Your answer: {answer}")
