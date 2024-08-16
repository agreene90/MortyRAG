
import unittest
import os
from src.knowledge_base import save_knowledge_base, load_knowledge_base
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

class TestKnowledgeBase(unittest.TestCase):

    def setUp(self):
        self.vectorizer = TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=2)
        self.vectors = np.array([[0.1, 0.2], [0.3, 0.4]])
        self.filenames = ["doc1.txt", "doc2.txt"]
        self.test_dir = "./test_data/"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def test_save_load_knowledge_base(self):
        save_knowledge_base(self.vectorizer, self.svd, self.vectors, self.filenames, self.test_dir)
        vectorizer, svd, vectors, filenames = load_knowledge_base(self.test_dir)

        self.assertTrue(np.array_equal(self.vectors, vectors), "Vectors should match after saving and loading.")
        self.assertEqual(self.filenames, filenames.tolist(), "Filenames should match after saving and loading.")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

if __name__ == "__main__":
    unittest.main()
