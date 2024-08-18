from data_ingestion import preprocess_documents
from knowledge_base import load_knowledge_base
from retrieval import retrieve_documents
from generation import ResponseGenerator
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_cached_model(data_directory="./data/processed"):
    """
    Load the model and other necessary components, with caching.
    
    Parameters:
    - data_directory: Path to the directory where the processed data is stored (default: "./data/processed").

    Returns:
    - vectorizer: The TF-IDF vectorizer.
    - svd: The SVD model used for dimensionality reduction.
    - vectors: The matrix of reduced document vectors.
    - filenames: A list of filenames corresponding to the document vectors.
    """
    try:
        logger.info("Loading knowledge base from directory: %s", data_directory)
        vectorizer, svd, vectors, filenames = load_knowledge_base(data_directory)
        logger.info("Knowledge base loaded successfully.")
        return vectorizer, svd, vectors, filenames
    except Exception as e:
        logger.error("Failed to load knowledge base: %s", str(e))
        raise RuntimeError("Error loading knowledge base.") from e

def main(query, cache):
    """
    Main function that processes the query and generates a response using cached models.
    
    Parameters:
    - query: The input query string.
    - cache: A dictionary to hold cached model components.
    
    Returns:
    - response: The generated response based on the query.
    """
    try:
        # Ensure the cache is populated with the necessary components
        if not all(cache.get(key) for key in ('vectorizer', 'svd', 'vectors', 'filenames')):
            logger.info("Cache is empty or incomplete, loading knowledge base...")
            cache['vectorizer'], cache['svd'], cache['vectors'], cache['filenames'] = load_cached_model()
        
        # Retrieve documents based on the query
        logger.info("Retrieving documents for query: '%s'", query)
        retrieved_docs = retrieve_documents(query, cache['vectorizer'], cache['svd'], cache['vectors'], cache['filenames'])
        
        # Instantiate the ResponseGenerator
        generator = ResponseGenerator()

        # Generate a response based on the retrieved documents
        logger.info("Generating response from retrieved documents...")
        response = generator.generate_response(retrieved_docs)
        
        logger.info("Response generation successful.")
        return response
    except Exception as e:
        logger.error("Error generating response: %s", str(e))
        raise RuntimeError("Error processing the query.") from e

if __name__ == "__main__":
    try:
        # Example query for testing
        query = "What is the history of quantum computing?"

        # Initialize cache for model and vectorizer
        model_cache = {
            'vectorizer': None,
            'svd': None,
            'vectors': None,
            'filenames': None
        }
        
        # Generate the response using the main function
        response = main(query, model_cache)
        
        # Output the generated response
        print("Generated Response:")
        print(response)
    
    except Exception as e:
        logger.error("An error occurred during execution: %s", str(e))
