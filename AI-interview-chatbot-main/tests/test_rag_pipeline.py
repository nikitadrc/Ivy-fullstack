# tests/test_rag_pipeline.py

import unittest
from unittest.mock import MagicMock
from src.rag_pipeline import build_vector_store_from_json, get_rag_chain, answer_query

class TestRAGPipeline(unittest.TestCase):

    def setUp(self):
        # Prepare a small sample JSON file for testing
        self.sample_json = "tests/sample_questions.json"
        with open(self.sample_json, "w", encoding="utf-8") as f:
            import json
            json.dump([
                {"question": "What is Python?", "model_answer": "Python is a programming language."},
                {"question": "Define OOP.", "model_answer": "OOP stands for Object-Oriented Programming."}
            ], f)
        self.vector_store = build_vector_store_from_json([self.sample_json])

    def test_vector_store_retrieval(self):
        # Test that the vector store can retrieve relevant chunks
        self.assertTrue(len(self.vector_store.index_to_docstore_id) > 0)

    def test_rag_chain_generation(self):
        # Mock the LLM to avoid API calls
        mock_llm = MagicMock()
        mock_llm.return_value = "Python is a programming language."
        rag_chain = get_rag_chain(self.vector_store)
        rag_chain.llm = mock_llm  # Patch the LLM
        answer, sources = answer_query(rag_chain, "Tell me about Python.")
        self.assertIn("Python", answer)

    def tearDown(self):
        import os
        os.remove(self.sample_json)

if __name__ == '__main__':
    unittest.main()
