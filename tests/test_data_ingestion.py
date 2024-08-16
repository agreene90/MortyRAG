
import unittest
import os
from src.data_ingestion import load_documents, preprocess_documents

class TestDataIngestion(unittest.TestCase):

    def test_load_documents(self):
        documents, filenames = load_documents('./data/raw/')
        self.assertGreater(len(documents), 0, "Documents should be loaded.")
        self.assertGreater(len(filenames), 0, "Filenames should be loaded.")

    def test_preprocess_documents(self):
        documents = ["THIS IS A TEST.", "New line\nHere"]
        processed_docs = preprocess_documents(documents)
        self.assertEqual(processed_docs[0], "this is a test.", "Documents should be lowercased.")
        self.assertNotIn("\n", processed_docs[1], "New lines should be removed.")

if __name__ == "__main__":
    unittest.main()
