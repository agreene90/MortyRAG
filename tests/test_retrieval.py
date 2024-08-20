import unittest
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from retrieval import retrieve_documents

class TestRetrieval(unittest.TestCase):

    def setUp(self):
        # Setup test data and directories
        self.vectorizer = TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=2)
        self.vectors = np.array([[0.1, 0.2], [0.3, 0.4]])
        self.filenames = ["doc1.txt", "doc2.txt"]
        self.test_dir = "./test_data/"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Fit vectorizer and SVD
        self.vectorizer.fit(["sample text for fitting"])
        self.svd.fit(self.vectorizer.transform(["sample text for fitting", "another text"]))
        
        # Save the fitted vectorizer, svd, and vectors as attributes
        self.fitted_vectorizer = self.vectorizer
        self.fitted_svd = self.svd
        self.fitted_vectors = self.vectors
        self.saved_filenames = self.filenames

    def test_retrieve_documents(self):
        # Test document retrieval
        retrieved_docs = retrieve_documents("sample text", self.fitted_vectorizer, self.fitted_svd, self.fitted_vectors, self.saved_filenames)
        
        self.assertTrue(len(retrieved_docs) > 0, "Should retrieve at least one document.")
        self.assertEqual(len(retrieved_docs), 2, "Should retrieve exactly two documents.")
    
    def test_empty_query(self):
        # Test empty query handling
        with self.assertRaises(ValueError):
            retrieve_documents("", self.fitted_vectorizer, self.fitted_svd, self.fitted_vectors, self.saved_filenames)

    def test_identical_similarity_scores(self):
        # Test handling of identical similarity scores
        identical_vectors = np.array([[0.1, 0.1], [0.1, 0.1]])
        retrieved_docs = retrieve_documents("sample text", self.fitted_vectorizer, self.fitted_svd, identical_vectors, self.saved_filenames)
        
        for _, sim in retrieved_docs:
            self.assertAlmostEqual(sim, 1.0, places=4, msg="All similarities should be identical when the vectors are the same.")

    def test_no_documents_retrieved(self):
        # Test case where no documents should be retrieved
        unrelated_query = "completely unrelated text"
        retrieved_docs = retrieve_documents(unrelated_query, self.fitted_vectorizer, self.fitted_svd, self.fitted_vectors, self.saved_filenames)
        
        self.assertEqual(len(retrieved_docs), 0, "No documents should be retrieved for an unrelated query.")

    def tearDown(self):
        # Clean up test data and directories
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

if __name__ == "__main__":
    unittest.main()
