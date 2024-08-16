import unittest
from controller import main

class TestRAGModel(unittest.TestCase):
    def test_response_generation(self):
        query = "What is the capital of France?"
        response = main(query)
        self.assertIn("Paris", response, "Response does not contain expected answer.")

    def test_empty_query(self):
        query = ""
        response = main(query)
        self.assertTrue(response, "Response should not be empty for a valid input.")
    
    def test_incorrect_query(self):
        query = "ajshdjkashdkjashd"
        response = main(query)
        self.assertTrue(response, "Model should return some response even for gibberish input.")

if __name__ == "__main__":
    unittest.main()
