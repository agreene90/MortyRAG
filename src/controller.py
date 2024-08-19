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
        logger.info(f"Loading knowledge base from directory: {data_directory}")
        vectorizer, svd, vectors, filenames = load_knowledge_base(data_directory)
        logger.info("Knowledge base loaded successfully.")
        return vectorizer, svd, vectors, filenames
    except FileNotFoundError as e:
        logger.error(f"Knowledge base files not found: {str(e)}")
        raise RuntimeError("Knowledge base files are missing. Please ensure the knowledge base is properly initialized.") from e
    except Exception as e:
        logger.error(f"Unexpected error while loading knowledge base: {str(e)}")
        raise RuntimeError("An unexpected error occurred while loading the knowledge base.") from e

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
        
        # Validate the query
        if not query.strip():
            raise ValueError("The query string is empty.")
        
        # Retrieve documents based on the query
        logger.info(f"Retrieving documents for query: '{query}'")
        retrieved_docs = retrieve_documents(query, cache['vectorizer'], cache['svd'], cache['vectors'], cache['filenames'])
        
        # Instantiate the ResponseGenerator
        generator = ResponseGenerator()

        # Generate a response based on the retrieved documents
        logger.info("Generating response from retrieved documents...")
        response = generator.generate_response(retrieved_docs)
        
        logger.info("Response generation successful.")
        return response
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during response generation: {str(e)}")
        raise RuntimeError("An unexpected error occurred while processing the query.") from e

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
        logger.error(f"An error occurred during execution: {str(e)}")
