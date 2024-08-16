import os
import pickle
import numpy as np

def save_knowledge_base(vectorizer, svd, vectors, filenames, filepath):
    with open(os.path.join(filepath, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    with open(os.path.join(filepath, 'svd.pkl'), 'wb') as f:
        pickle.dump(svd, f)
    
    np.save(os.path.join(filepath, 'reduced_vectors.npy'), vectors)
    np.save(os.path.join(filepath, 'filenames.npy'), filenames)

def load_knowledge_base(filepath):
    with open(os.path.join(filepath, 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
        
    with open(os.path.join(filepath, 'svd.pkl'), 'rb') as f:
        svd = pickle.load(f)
    
    vectors = np.load(os.path.join(filepath, 'reduced_vectors.npy'))
    filenames = np.load(os.path.join(filepath, 'filenames.npy'))
    
    return vectorizer, svd, vectors, filenames

if __name__ == "__main__":
    vectorizer, svd, vectors, filenames = load_knowledge_base("./processed_data")
    print("Knowledge Base Loaded Successfully")
