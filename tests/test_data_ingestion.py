import unittest
import os
import logging
from src.data_ingestion import load_documents, preprocess_documents

# Setup logging for the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDataIngestion(unittest.TestCase):

    def setUp(self):
        """
        Setup for the tests, such as defining test data paths.
        """
        self.test_data_dir = './test_data/'
        self.test_documents = ["THIS IS A TEST.", "New line\nHere"]
        self.expected_processed_docs = ["this is a test.", "new line here"]

        # Create a temporary test directory and files if they don't exist
        os.makedirs(self.test_data_dir, exist_ok=True)
        with open(os.path.join(self.test_data_dir, 'test1.txt'), 'w', encoding='utf-8') as f:
            f.write(self.test_documents[0])
        with open(os.path.join(self.test_data_dir, 'test2.txt'), 'w', encoding='utf-8') as f:
            f.write(self.test_documents[1])
        
        logger.info(f"Test data created in {self.test_data_dir}")

    def test_load_documents(self):
        """
        Test loading of documents from a directory.
        """
        try:
            documents, filenames = load_documents(self.test_data_dir)
            logger.info(f"Loaded documents: {documents}")
            logger.info(f"Loaded filenames: {filenames}")

            self.assertGreater(len(documents), 0, "Documents should be loaded.")
            self.assertGreater(len(filenames), 0, "Filenames should be loaded.")
            self.assertIn("test1.txt", filenames, "Filename 'test1.txt' should be in the loaded filenames.")
            self.assertIn("test2.txt", filenames, "Filename 'test2.txt' should be in the loaded filenames.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_preprocess_documents(self):
        """
        Test preprocessing of document text (lowercasing, removing new lines).
        """
        try:
            processed_docs = preprocess_documents(self.test_documents)
            logger.info(f"Processed documents: {processed_docs}")

            self.assertEqual(processed_docs, self.expected_processed_docs, "Processed documents should match expected output.")
            self.assertNotIn("\n", processed_docs[1], "New lines should be removed from the documents.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        try:
            for file in os.listdir(self.test_data_dir):
                file_path = os.path.join(self.test_data_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")
            os.rmdir(self.test_data_dir)
            logger.info(f"Deleted test directory: {self.test_data_dir}")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    unittest.main()
