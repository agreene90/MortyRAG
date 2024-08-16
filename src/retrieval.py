import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import load_knowledge_base

def retrieve_documents(query, vectorizer, svd, vectors, filenames, top_k=5):
    query_vec = vectorizer.transform([query])
    reduced_query_vec = svd.transform(query_vec)
    
    similarities = cosine_similarity(reduced_query_vec, vectors).flatten()
    
    ranked_indices = np.argsort(similarities)[-top_k:][::-1]
    
    retrieved_docs = [(filenames[i], similarities[i]) for i in ranked_indices]
    
    return retrieved_docs

if __name__ == "__main__":
    query = "Tell me about the Eiffel Tower"
    vectorizer, svd, vectors, filenames = load_knowledge_base("./processed_data")
    
    retrieved_docs = retrieve_documents(query, vectorizer, svd, vectors, filenames)
    print("Top retrieved documents:")
    for doc in retrieved_docs:
        print(f"Document: {doc[0]}, Similarity: {doc[1]:.4f}")
