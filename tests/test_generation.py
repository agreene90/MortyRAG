import unittest
from src.generation import ResponseGenerator
import logging

# Setup logging for the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestResponseGenerator(unittest.TestCase):

    def setUp(self):
        """
        Setup the ResponseGenerator instance before each test.
        """
        self.generator = ResponseGenerator()
        logger.info("Initialized ResponseGenerator instance for testing.")

    def test_generate_response(self):
        """
        Test generating a response from a list of retrieved documents.
        """
        try:
            retrieved_docs = [
                ("Document1", "This is content from document 1."),
                ("Document2", "This is content from document 2.")
            ]
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response: {response}")
            self.assertTrue(len(response) > 0, "The response should not be empty.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_generate_response_with_no_docs(self):
        """
        Test generating a response when no documents are provided.
        """
        try:
            retrieved_docs = []
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response for empty document list: {response}")
            self.assertTrue(response, "The response should gracefully handle an empty document list.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_generate_response_with_long_input(self):
        """
        Test generating a response when documents contain long text.
        """
        try:
            retrieved_docs = [
                ("Document1", "This is content from document 1."),
                ("Document2", "This is a very long content from document 2. " * 100)
            ]
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response for long input: {response}")
            self.assertTrue(len(response) > 0, "The response should handle long input texts.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_generate_response_special_characters(self):
        """
        Test generating a response when documents contain special characters.
        """
        try:
            retrieved_docs = [
                ("Document1", "@@@$$$!!! This document contains special characters.")
            ]
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response for special characters: {response}")
            self.assertTrue(len(response) > 0, "The response should handle documents with special characters.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_generate_response_with_unicode(self):
        """
        Test generating a response when documents contain Unicode characters.
        """
        try:
            retrieved_docs = [
                ("Document1", "This is content with Unicode characters: 測試, тест, اختبار.")
            ]
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response for Unicode content: {response}")
            self.assertTrue(len(response) > 0, "The response should handle documents with Unicode characters.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_generate_response_with_empty_strings(self):
        """
        Test generating a response when documents contain empty strings.
        """
        try:
            retrieved_docs = [
                ("Document1", "")
            ]
            response = self.generator.generate_response(retrieved_docs)
            logger.info(f"Generated response for empty string: {response}")
            self.assertTrue(len(response) > 0, "The response should handle documents with empty strings gracefully.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

if __name__ == "__main__":
    unittest.main()