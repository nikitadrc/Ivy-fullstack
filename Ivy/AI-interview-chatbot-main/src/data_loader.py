# src/data_loader.py

import json
import os

def load_questions(
    technical_path="data/technical_questions.json",
    behavioral_path="data/behavioral_questions.json",
    hr_path="data/hr_questions.json"
):
    """
    Load and combine technical, behavioral, and HR questions from JSON files.

    Returns:
        questions (list): List of dicts with keys: 'category', 'text', 'model_answer'
    """
    questions = []

    # Helper to load a single category
    def load_category(path, category_name):
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Assume each entry has 'question' and 'model_answer' keys
        return [
            {
                "category": category_name,
                "text": q.get("question", ""),
                "model_answer": q.get("model_answer", "")
            }
            for q in data
        ]

    questions += load_category(technical_path, "Technical")
    questions += load_category(behavioral_path, "Behavioral")
    questions += load_category(hr_path, "HR")

    return questions

def save_questions(questions, out_path="data/all_questions.json"):
    """
    Save the combined questions list to a JSON file.
    """
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

# Example usage (for testing/demo)
if __name__ == "__main__":
    questions = load_questions()
    print(f"Loaded {len(questions)} questions.")
    print("Sample:", questions[0] if questions else "No questions found.")
    save_questions(questions)
