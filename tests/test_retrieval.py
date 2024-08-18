import unittest
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from retrieval import retrieve_documents
from knowledge_base import save_knowledge_base, load_knowledge_base

class TestRetrieval(unittest.TestCase):

    def setUp(self):
        # Setup a mock knowledge base with fitted vectorizer and SVD
        self.vectorizer = TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=2)
        sample_data = ["sample text for fitting", "another example document"]
        self.vectors = self.svd.fit_transform(self.vectorizer.fit_transform(sample_data))
        self.filenames = ["doc1.txt", "doc2.txt"]
        self.test_dir = "./test_data/"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        save_knowledge_base(self.vectorizer, self.svd, self.vectors, self.filenames, self.test_dir)

    def test_retrieve_documents(self):
        vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)
        retrieved_docs = retrieve_documents("sample text", vectorizer, svd, vectors, filenames)
        
        self.assertTrue(len(retrieved_docs) > 0, "Should retrieve at least one document.")
        self.assertEqual(retrieved_docs[0][0], "doc1.txt", "The most relevant document should be retrieved first.")

    def test_empty_query(self):
        vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)
        with self.assertRaises(ValueError):
            retrieve_documents("", vectorizer, svd, vectors, filenames)

    def test_identical_similarity_scores(self):
        # Test for identical similarity scores to ensure correct handling
        identical_vectors = np.array([[0.1, 0.1], [0.1, 0.1]])
        vectorizer, svd, _, filenames = load_knowledge_base(self.test_dir)
        retrieved_docs = retrieve_documents("sample text", vectorizer, svd, identical_vectors, filenames)
        
        for _, sim in retrieved_docs:
            self.assertEqual(sim, 0.0, "All similarities should be zero when the scores are identical.")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

if __name__ == "__main__":
    unittest.main()
