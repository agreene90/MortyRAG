
import unittest
from controller import main

class TestRAGModel(unittest.TestCase):

    def test_response_generation(self):
        query = "What is the capital of France?"
        response = main(query)
        self.assertIn("Paris", response, "The response should include 'Paris'.")

    def test_empty_query(self):
        query = ""
        response = main(query)
        self.assertTrue(response, "Response should handle empty queries gracefully.")

    def test_incorrect_query(self):
        query = "ajshdjkashdkjashd"
        response = main(query)
        self.assertTrue(response, "Response should handle gibberish queries gracefully.")

    def test_query_with_special_characters(self):
        query = "@@@$$$!!!"
        response = main(query)
        self.assertTrue(response, "Response should handle special characters in the query.")

    def test_numeric_query(self):
        query = "1234567890"
        response = main(query)
        self.assertTrue(response, "Response should handle numeric queries.")

    def test_long_query(self):
        query = "Explain the theory of relativity in detail and provide examples, history, and implications in modern science."
        response = main(query)
        self.assertTrue(len(response) > 0, "Response should be generated for long queries.")

    def test_query_with_database_retrieval(self):
        query = "Tell me about the project files."
        response = main(query)
        self.assertIn("file", response.lower(), "The response should reference files from the database.")

if __name__ == "__main__":
    unittest.main()
