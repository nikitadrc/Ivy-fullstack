# tests/test_data_loader.py

import unittest
import os
import json
from src.data_loader import load_questions

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Create sample JSON files for testing
        self.test_dir = "tests/tmp_data/"
        os.makedirs(self.test_dir, exist_ok=True)
        self.tech_file = os.path.join(self.test_dir, "technical_questions.json")
        self.beh_file = os.path.join(self.test_dir, "behavioral_questions.json")
        self.hr_file = os.path.join(self.test_dir, "hr_questions.json")

        tech_data = [
            {"question": "What is OOP?", "model_answer": "Object-Oriented Programming..."}
        ]
        beh_data = [
            {"question": "Describe a challenge you faced.", "model_answer": "I once..."}
        ]
        hr_data = [
            {"question": "Why do you want this job?", "model_answer": "Because..."}
        ]
        with open(self.tech_file, "w", encoding="utf-8") as f:
            json.dump(tech_data, f)
        with open(self.beh_file, "w", encoding="utf-8") as f:
            json.dump(beh_data, f)
        with open(self.hr_file, "w", encoding="utf-8") as f:
            json.dump(hr_data, f)

    def tearDown(self):
        # Clean up test files
        for file in [self.tech_file, self.beh_file, self.hr_file]:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_load_questions_all_present(self):
        questions = load_questions(
            technical_path=self.tech_file,
            behavioral_path=self.beh_file,
            hr_path=self.hr_file
        )
        self.assertEqual(len(questions), 3)
        categories = set(q['category'] for q in questions)
        self.assertSetEqual(categories, {"Technical", "Behavioral", "HR"})
        self.assertIn("text", questions[0])
        self.assertIn("model_answer", questions[0])

    def test_load_questions_missing_file(self):
        # Remove one file and test
        os.remove(self.hr_file)
        questions = load_questions(
            technical_path=self.tech_file,
            behavioral_path=self.beh_file,
            hr_path=self.hr_file
        )
        self.assertEqual(len(questions), 2)
        categories = set(q['category'] for q in questions)
        self.assertSetEqual(categories, {"Technical", "Behavioral"})

    def test_load_questions_empty_file(self):
        # Write empty JSON to one file
        with open(self.beh_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        questions = load_questions(
            technical_path=self.tech_file,
            behavioral_path=self.beh_file,
            hr_path=self.hr_file
        )
        self.assertEqual(len(questions), 2)  # Only tech and hr have data

if __name__ == "__main__":
    unittest.main()
