import unittest
import sys
import os
import logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controller import main  # Import the main function from controller.py

# Setup logging for the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestController(unittest.TestCase):

    def setUp(self):
        """
        Setup a cache to be used across all test cases.
        """
        self.cache = {
            'vectorizer': None,
            'svd': None,
            'vectors': None,
            'filenames': None
        }

    def test_response_generation(self):
        """
        Test that the controller generates an appropriate response for a valid query.
        """
        query = "What is the capital of France?"
        try:
            response = main(query, self.cache)
            logger.info(f"Response: {response}")
            self.assertIn("paris", response.lower(), "The response should include 'Paris'.")
            self.assertGreater(len(response), 0, "Response should not be empty.")
        except Exception as e:
            logger.error(f"Test failed with exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_empty_query(self):
        """
        Test that the controller raises an error when an empty query is provided.
        """
        query = ""
        with self.assertRaises(ValueError):
            main(query, self.cache)

    def test_incorrect_query(self):
        """
        Test how the controller handles a nonsensical query.
        """
        query = "ajshdjkashdkjashd"
        response = main(query, self.cache)
        logger.info(f"Response to incorrect query: {response}")
        self.assertIn("not found", response.lower(), "Response should indicate that no results were found.")

    def test_query_with_special_characters(self):
        """
        Test how the controller handles a query with special characters.
        """
        query = "@@@$$$!!!"
        response = main(query, self.cache)
        logger.info(f"Response to special characters query: {response}")
        self.assertIn("error", response.lower(), "Response should handle and indicate errors with special characters.")

    def test_numeric_query(self):
        """
        Test how the controller handles a numeric query.
        """
        query = "1234567890"
        response = main(query, self.cache)
        logger.info(f"Response to numeric query: {response}")
        self.assertNotIn("error", response.lower(), "Response should handle numeric queries gracefully.")
        self.assertGreater(len(response), 0, "Response should not be empty for numeric queries.")

    def test_long_query(self):
        """
        Test the controller's handling of a long and complex query.
        """
        query = "Explain the theory of relativity in detail and provide examples, history, and implications in modern science."
        response = main(query, self.cache)
        logger.info(f"Response to long query: {response}")
        self.assertIn("theory", response.lower(), "Response should reference key concepts from the query.")
        self.assertGreater(len(response), 0, "Response should not be empty for long queries.")

    def test_query_with_database_retrieval(self):
        """
        Test that the controller can retrieve and reference files from the database in the response.
        """
        query = "Tell me about the project files."
        response = main(query, self.cache)
        logger.info(f"Response to database retrieval query: {response}")
        self.assertIn("file", response.lower(), "The response should reference files from the database.")
        self.assertGreater(len(response), 0, "Response should not be empty when querying the database.")

if __name__ == "__main__":
    unittest.main()
