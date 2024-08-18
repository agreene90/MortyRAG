import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import load_knowledge_base

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_documents(query, vectorizer, svd, vectors, filenames, top_k=5, normalize=True):
    """
    Retrieve the top-k documents most similar to the query.
    
    Parameters:
    - query: The input query string.
    - vectorizer: The vectorizer used to transform the query.
    - svd: The dimensionality reduction model (e.g., SVD).
    - vectors: The matrix of document vectors.
    - filenames: List of filenames corresponding to the document vectors.
    - top_k: Number of top documents to retrieve (default is 5).
    - normalize: Whether to normalize similarity scores (default is True).
    
    Returns:
    - A list of tuples with the top-k filenames and their corresponding similarity scores.
    """
    if not query.strip():
        raise ValueError("The query string is empty.")
    
    try:
        logger.info("Transforming the query into vector space...")
        query_vec = vectorizer.transform([query])
        reduced_query_vec = svd.transform(query_vec)
        
        logger.info("Computing cosine similarities...")
        similarities = cosine_similarity(reduced_query_vec, vectors).flatten()
        
        if normalize:
            if np.all(similarities == similarities[0]):
                logger.warning("All similarity scores are identical; skipping normalization.")
            else:
                similarities = (similarities - similarities.min()) / (similarities.max() - similarities.min())
        
        logger.info("Ranking documents based on similarity scores...")
        ranked_indices = np.argsort(similarities)[-top_k:][::-1]
        
        retrieved_docs = [(filenames[i], similarities[i]) for i in ranked_indices]
        
        logger.info(f"Retrieved top {top_k} documents successfully.")
        return retrieved_docs
    
    except Exception as e:
        logger.error(f"Error during document retrieval: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        query = "Tell me about the Eiffel Tower"
        logger.info(f"Loading knowledge base...")
        vectorizer, svd, vectors, filenames = load_knowledge_base("./data/processed")
        
        logger.info(f"Retrieving documents for query: '{query}'")
        retrieved_docs = retrieve_documents(query, vectorizer, svd, vectors, filenames, top_k=5)
        
        print("Top retrieved documents:")
        for doc in retrieved_docs:
            print(f"Document: {doc[0]}, Similarity: {doc[1]:.4f}")
    
    except Exception as e:
        logger.error(f"An error occurred in the retrieval process: {str(e)}")
