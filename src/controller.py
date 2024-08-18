from data_ingestion import preprocess_documents
from knowledge_base import load_knowledge_base
from retrieval import retrieve_documents
from generation import ResponseGenerator  # Import the ResponseGenerator class
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_cached_model(data_directory="./data/processed"):
    """
    Load the model and other necessary components, with caching.
    """
    try:
        logger.info("Loading knowledge base...")
        vectorizer, svd, vectors, filenames = load_knowledge_base(data_directory)
        logger.info("Knowledge base loaded successfully.")
        return vectorizer, svd, vectors, filenames
    except Exception as e:
        logger.error("Failed to load knowledge base: %s", str(e))
        raise RuntimeError("Error loading knowledge base.") from e

def main(query, cache):
    """
    Main function that processes the query and generates a response using cached models.
    """
    try:
        # Check if the cache is already populated
        if not all(key in cache for key in ('vectorizer', 'svd', 'vectors', 'filenames')):
            logger.info("Cache is empty or incomplete, loading data...")
            cache['vectorizer'], cache['svd'], cache['vectors'], cache['filenames'] = load_cached_model()
        
        # Retrieve documents based on the query
        retrieved_docs = retrieve_documents(query, cache['vectorizer'], cache['svd'], cache['vectors'], cache['filenames'])
        
        # Instantiate the ResponseGenerator
        generator = ResponseGenerator()

        # Generate a response based on the retrieved documents
        response = generator.generate_response(retrieved_docs)
        
        return response
    except Exception as e:
        logger.error("Error generating response: %s", str(e))
        raise RuntimeError("Error processing the query.") from e

if __name__ == "__main__":
    # Example query for testing
    query = "What is the history of the Eiffel Tower?"

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
