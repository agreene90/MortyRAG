import os
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def load_documents(directory):
    documents = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                documents.append(f.read())
                filenames.append(filename)
    return documents, filenames

def preprocess_documents(documents):
    processed_docs = [doc.lower().replace('\n', ' ').replace('\r', '').strip() for doc in documents]
    return processed_docs

def vectorize_documents(documents, n_components=100):
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    vectors = vectorizer.fit_transform(documents)
    svd = TruncatedSVD(n_components=n_components)
    reduced_vectors = svd.fit_transform(vectors)
    return vectorizer, svd, reduced_vectors

def save_preprocessed_data(vectorizer, svd, vectors, filenames, directory):
    np.save(os.path.join(directory, 'reduced_vectors.npy'), vectors)
    np.save(os.path.join(directory, 'filenames.npy'), np.array(filenames))
    
    with open(os.path.join(directory, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    with open(os.path.join(directory, 'svd.pkl'), 'wb') as f:
        pickle.dump(svd, f)

if __name__ == "__main__":
    data_directory = "./data"
    save_directory = "./processed_data"
    os.makedirs(save_directory, exist_ok=True)

    documents, filenames = load_documents(data_directory)
    preprocessed_docs = preprocess_documents(documents)
    vectorizer, svd, vectors = vectorize_documents(preprocessed_docs)
    
    save_preprocessed_data(vectorizer, svd, vectors, filenames, save_directory)
