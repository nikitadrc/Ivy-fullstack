# src/evaluation.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Efficient model loading (singleton pattern)
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def evaluate_answer(answer, model_answer):
    """
    Evaluate a candidate's answer against the model answer using semantic similarity.

    Args:
        answer (str): Candidate's answer.
        model_answer (str): Reference/model answer.

    Returns:
        score (float): Score between 0 and 5.
        feedback (str): Textual feedback.
    """
    if not answer or not answer.strip():
        return 0.0, "No answer provided."

    model = get_model()
    embeddings = model.encode([answer, model_answer])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # Map similarity (0 to 1) to score (0 to 5)
    score = round(similarity * 5, 2)

    feedback = generate_feedback(answer, score, model_answer)
    return score, feedback

def generate_feedback(candidate_answer, score, model_answer):
    """
    Generate feedback based on the score and model answer.
    Optionally, can be extended to include more advanced feedback logic.

    Args:
        candidate_answer (str): Candidate's answer.
        score (float): Score between 0 and 5.
        model_answer (str): Reference/model answer.

    Returns:
        feedback (str)
    """
    # Optionally, you could add keyword/phrase checking or LLM-based feedback here
    if score >= 4.0:
        return "Excellent answer! You covered all key points."
    elif score >= 3.0:
        return f"Good answer. To improve, consider including more details such as: {model_answer}"
    elif score >= 2.0:
        return f"Fair attempt, but your answer could be more comprehensive. Key points: {model_answer}"
    elif score > 0:
        return f"Your answer lacks important details. Review the topic and try to include: {model_answer}"
    else:
        return "No answer provided or answer is not relevant."

# Optional: For session state/history tracking in Streamlit
def record_answer_history(question, candidate_answer, model_answer, score, feedback, sentiment, session_state):
    """
    Record the answer and feedback to the session history for analytics or review.
    """
    if 'answer_history' not in session_state:
        session_state['answer_history'] = []
    session_state['answer_history'].append({
        "question": question,
        "candidate_answer": candidate_answer,
        "model_answer": model_answer,
        "score": score,
        "feedback": feedback,
        "sentiment": sentiment
    })

# Example usage (for testing/demo)
if __name__ == "__main__":
    candidate_answer = "OOP is a way to structure programs using objects and classes."
    model_answer = "Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects, which can contain data and code to manipulate that data."
    score, feedback = evaluate_answer(candidate_answer, model_answer)
    print(f"Score: {score}\nFeedback: {feedback}")
