# tests/test_chatbot.py

import unittest
from unittest.mock import patch

from src.evaluation import evaluate_answer
from src.sentiment_analysis import analyze_sentiment
from src.human_handoff import handle_human_handoff

class TestChatbotCore(unittest.TestCase):

    def test_evaluate_answer_perfect(self):
        candidate_answer = "Object-Oriented Programming is a paradigm based on objects and classes."
        model_answer = "Object-Oriented Programming (OOP) is a paradigm based on objects and classes."
        score, feedback = evaluate_answer(candidate_answer, model_answer)
        self.assertGreaterEqual(score, 4.0)
        self.assertIn("Excellent", feedback)

    def test_evaluate_answer_poor(self):
        candidate_answer = "I don't know."
        model_answer = "OOP is about objects and classes."
        score, feedback = evaluate_answer(candidate_answer, model_answer)
        self.assertLessEqual(score, 2.0)
        self.assertIn("lacks important details", feedback)

    def test_sentiment_analysis_positive(self):
        text = "I am very happy with this interview process!"
        result = analyze_sentiment(text)
        self.assertEqual(result['label'], 'Positive')

    def test_sentiment_analysis_negative(self):
        text = "This is terrible and confusing."
        result = analyze_sentiment(text)
        self.assertEqual(result['label'], 'Negative')

    @patch('src.human_handoff.detect_handoff_need', return_value=True)
    def test_human_handoff_trigger(self, mock_detect):
        candidate_response = "I want to talk to a human."
        sentiment = "Negative"
        context = {"candidate_id": "test123", "name": "Test User"}
        triggered = handle_human_handoff(candidate_response, sentiment, context)
        self.assertTrue(triggered)

if __name__ == '__main__':
    unittest.main()
