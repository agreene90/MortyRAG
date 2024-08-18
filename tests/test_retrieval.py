import unittest
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from retrieval import retrieve_documents
from knowledge_base import save_knowledge_base, load_knowledge_base

class TestRetrieval(unittest.TestCase):

    def setUp(self):
        self.vectorizer = TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=2)
        self.vectors = np.array([[0.1, 0.2], [0.3, 0.4]])
        self.filenames = ["doc1.txt", "doc2.txt"]
        self.test_dir = "./test_data/"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        self.vectorizer.fit(["sample text for fitting"])
        save_knowledge_base(self.vectorizer, self.svd, self.vectors, self.filenames, self.test_dir)

    def test_retrieve_documents(self):
        vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)
        retrieved_docs = retrieve_documents("sample text", vectorizer, svd, vectors, filenames)
        
        self.assertTrue(len(retrieved_docs) > 0, "Should retrieve at least one document.")
    
    def test_empty_query(self):
        vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)
        with self.assertRaises(ValueError):
            retrieve_documents("", vectorizer, svd, vectors, filenames)

    def test_identical_similarity_scores(self):
        identical_vectors = np.array([[0.1, 0.1], [0.1, 0.1]])
        vectorizer, svd, _, filenames = load_knowledge_base(self.test_dir)
        retrieved_docs = retrieve_documents("sample text", vectorizer, svd, identical_vectors, filenames)
        
        for _, sim in retrieved_docs:
            self.assertEqual(sim, 1.0, "All similarities should be identical when the vectors are the same.")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

if __name__ == "__main__":
    unittest.main()
