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
        
        if svd is not None:
            reduced_query_vec = svd.transform(query_vec)
        else:
            logger.warning("SVD model is not provided; skipping dimensionality reduction.")
            reduced_query_vec = query_vec
        
        logger.info("Computing cosine similarities...")
        similarities = cosine_similarity(reduced_query_vec, vectors).flatten()
        
        if similarities.size == 0:
            logger.warning("No similarities were computed, returning an empty result.")
            return []
        
        if normalize:
            if np.all(similarities == similarities[0]):
                logger.warning("All similarity scores are identical; skipping normalization.")
            else:
                similarities = (similarities - similarities.min()) / (similarities.max() - similarities.min())
        
        logger.info("Ranking documents based on similarity scores...")
        ranked_indices = np.argsort(similarities)[-top_k:][::-1]
        
        retrieved_docs = [(filenames[i], similarities[i]) for i in ranked_indices if similarities[i] > 0]
        
        if not retrieved_docs:
            logger.warning("No documents with non-zero similarity scores were found.")
        
        logger.info(f"Retrieved top {len(retrieved_docs)} documents successfully.")
        return retrieved_docs
    
    except Exception as e:
        logger.error(f"Error during document retrieval: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        queries = [
            "Explain quantum computing and its applications.",
            "Discuss the history of the Roman Empire."
        ]
        
        logger.info("Loading knowledge base...")
        vectorizer, svd, vectors, filenames = load_knowledge_base("./data/processed")
        
        if not vectors.size or not filenames:
            logger.error("Knowledge base appears to be empty or improperly loaded.")
        else:
            for query in queries:
                logger.info(f"Retrieving documents for query: '{query}'")
                retrieved_docs = retrieve_documents(query, vectorizer, svd, vectors, filenames, top_k=5)
                
                if retrieved_docs:
                    print(f"\nTop retrieved documents for query '{query}':")
                    for doc in retrieved_docs:
                        print(f"Document: {doc[0]}, Similarity: {doc[1]:.4f}")
                else:
                    print(f"No relevant documents found for query '{query}'.")
    
    except Exception as e:
        logger.error(f"An error occurred in the retrieval process: {str(e)}")
