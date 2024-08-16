
import unittest
from src.generation import ResponseGenerator

class TestGeneration(unittest.TestCase):

    def setUp(self):
        self.generator = ResponseGenerator()

    def test_generate_response(self):
        retrieved_docs = [("Document1", "This is content from document 1."), ("Document2", "This is content from document 2.")]
        response = self.generator.generate_response(retrieved_docs)
        self.assertTrue(len(response) > 0, "Response should be generated for the retrieved documents.")

if __name__ == "__main__":
    unittest.main()
