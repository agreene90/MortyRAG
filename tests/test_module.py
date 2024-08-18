import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controller import main  # Import the main function from controller.py

class TestRAGModel(unittest.TestCase):

    def setUp(self):
        # Initialize a cache for each test
        self.cache = {
            'vectorizer': None,
            'svd': None,
            'vectors': None,
            'filenames': None
        }

    def test_response_generation(self):
        query = "What is the capital of France?"
        response = main(query, self.cache)
        self.assertIn("paris", response.lower(), "The response should include 'Paris'.")
        self.assertGreater(len(response), 0, "Response should not be empty.")

    def test_empty_query(self):
        query = ""
        with self.assertRaises(ValueError):
            main(query, self.cache)

    def test_incorrect_query(self):
        query = "ajshdjkashdkjashd"
        response = main(query, self.cache)
        self.assertIn("not found", response.lower(), "Response should indicate that no results were found.")

    def test_query_with_special_characters(self):
        query = "@@@$$$!!!"
        response = main(query, self.cache)
        self.assertIn("error", response.lower(), "Response should handle and indicate errors with special characters.")

    def test_numeric_query(self):
        query = "1234567890"
        response = main(query, self.cache)
        self.assertNotIn("error", response.lower(), "Response should handle numeric queries gracefully.")

    def test_long_query(self):
        query = "Explain the theory of relativity in detail and provide examples, history, and implications in modern science."
        response = main(query, self.cache)
        self.assertIn("theory", response.lower(), "Response should reference key concepts from the query.")

    def test_query_with_database_retrieval(self):
        query = "Tell me about the project files."
        response = main(query, self.cache)
        self.assertIn("file", response.lower(), "The response should reference files from the database.")

if __name__ == "__main__":
    unittest.main()
