import unittest
from generation import ResponseGenerator

class TestResponseGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ResponseGenerator()

    def test_generate_response(self):
        retrieved_docs = [
            ("Document1", "This is content from document 1."),
            ("Document2", "This is content from document 2.")
        ]
        response = self.generator.generate_response(retrieved_docs)
        self.assertTrue(len(response) > 0, "The response should not be empty.")

    def test_generate_response_with_no_docs(self):
        retrieved_docs = []
        response = self.generator.generate_response(retrieved_docs)
        self.assertTrue(response, "The response should gracefully handle empty document list.")

    def test_generate_response_with_long_input(self):
        retrieved_docs = [
            ("Document1", "This is content from document 1."),
            ("Document2", "This is a very long content from document 2. " * 100)
        ]
        response = self.generator.generate_response(retrieved_docs)
        self.assertTrue(len(response) > 0, "The response should handle long input texts.")

    def test_generate_response_special_characters(self):
        retrieved_docs = [
            ("Document1", "@@@$$$!!!")
        ]
        response = self.generator.generate_response(retrieved_docs)
        self.assertIn("error", response.lower(), "The response should indicate errors with special characters.")

if __name__ == "__main__":
    unittest.main()
