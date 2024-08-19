import unittest
import os
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from src.knowledge_base import save_knowledge_base, load_knowledge_base

# Setup logging for the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestKnowledgeBase(unittest.TestCase):

    def setUp(self):
        """
        Set up test variables and directories before each test.
        """
        self.vectorizer = TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=2)
        self.vectors = np.array([[0.1, 0.2], [0.3, 0.4]])
        self.filenames = ["doc1.txt", "doc2.txt"]
        self.test_dir = "./test_data/"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            logger.info(f"Created test directory: {self.test_dir}")

    def test_save_load_knowledge_base(self):
        """
        Test saving and loading of the knowledge base.
        """
        try:
            # Save the knowledge base
            save_knowledge_base(self.vectorizer, self.svd, self.vectors, self.filenames, self.test_dir)
            logger.info("Knowledge base saved successfully.")

            # Load the knowledge base
            vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)
            logger.info("Knowledge base loaded successfully.")

            # Assert that saved and loaded data match
            self.assertTrue(np.array_equal(self.vectors, vectors), "Vectors should match after saving and loading.")
            self.assertEqual(self.filenames, filenames.tolist(), "Filenames should match after saving and loading.")
            self.assertIsInstance(vectorizer, TfidfVectorizer, "Loaded vectorizer should be an instance of TfidfVectorizer.")
            self.assertIsInstance(svd, TruncatedSVD, "Loaded SVD model should be an instance of TruncatedSVD.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_save_load_empty_knowledge_base(self):
        """
        Test saving and loading of an empty knowledge base.
        """
        try:
            empty_vectors = np.array([])
            empty_filenames = []

            # Save the empty knowledge base
            save_knowledge_base(self.vectorizer, self.svd, empty_vectors, empty_filenames, self.test_dir)
            logger.info("Empty knowledge base saved successfully.")

            # Load the empty knowledge base
            _, _, loaded_vectors, loaded_filenames = load_knowledge_base(self.test_dir)
            logger.info("Empty knowledge base loaded successfully.")

            # Assert that the loaded data matches the saved empty data
            self.assertTrue(np.array_equal(empty_vectors, loaded_vectors), "Vectors should match after saving and loading.")
            self.assertEqual(empty_filenames, loaded_filenames.tolist(), "Filenames should match after saving and loading.")
            self.assertEqual(len(loaded_vectors), 0, "Loaded vectors should be empty.")
            self.assertEqual(len(loaded_filenames), 0, "Loaded filenames should be empty.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def test_invalid_load(self):
        """
        Test loading from an invalid or non-existent directory.
        """
        try:
            with self.assertRaises(RuntimeError):
                load_knowledge_base("./non_existent_directory")
            logger.info("Properly handled invalid load attempt.")
        except Exception as e:
            logger.error(f"Test failed due to an exception: {str(e)}")
            self.fail(f"Test encountered an exception: {str(e)}")

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)
            logger.info(f"Deleted test directory: {self.test_dir}")

if __name__ == "__main__":
    unittest.main()