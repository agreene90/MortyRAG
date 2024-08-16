import os
import pickle
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_knowledge_base(vectorizer, svd, vectors, filenames, filepath):
    """
    Save the components of the knowledge base to the specified filepath.
    
    Parameters:
    - vectorizer: The vectorizer used to transform documents.
    - svd: The SVD model used for dimensionality reduction.
    - vectors: The matrix of reduced document vectors.
    - filenames: List of filenames corresponding to the document vectors.
    - filepath: The directory where the knowledge base components will be saved.
    """
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            logger.info(f"Created directory: {filepath}")

        logger.info("Saving vectorizer...")
        with open(os.path.join(filepath, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)
            
        logger.info("Saving SVD model...")
        with open(os.path.join(filepath, 'svd.pkl'), 'wb') as f:
            pickle.dump(svd, f)
        
        logger.info("Saving reduced document vectors...")
        np.save(os.path.join(filepath, 'reduced_vectors.npy'), vectors)
        
        logger.info("Saving filenames list...")
        np.save(os.path.join(filepath, 'filenames.npy'), filenames)
        
        logger.info("Knowledge base saved successfully.")
    
    except Exception as e:
        logger.error(f"Error saving knowledge base: {str(e)}")
        raise

def load_knowledge_base(filepath):
    """
    Load the components of the knowledge base from the specified filepath.
    
    Parameters:
    - filepath: The directory where the knowledge base components are stored.
    
    Returns:
    - vectorizer: The loaded vectorizer.
    - svd: The loaded SVD model.
    - vectors: The loaded matrix of reduced document vectors.
    - filenames: The loaded list of filenames.
    """
    try:
        logger.info("Loading vectorizer...")
        with open(os.path.join(filepath, 'vectorizer.pkl'), 'rb') as f:
            vectorizer = pickle.load(f)
            
        logger.info("Loading SVD model...")
        with open(os.path.join(filepath, 'svd.pkl'), 'rb') as f:
            svd = pickle.load(f)
        
        logger.info("Loading reduced document vectors...")
        vectors = np.load(os.path.join(filepath, 'reduced_vectors.npy'))
        
        logger.info("Loading filenames list...")
        filenames = np.load(os.path.join(filepath, 'filenames.npy'))
        
        logger.info("Knowledge base loaded successfully.")
        return vectorizer, svd, vectors, filenames
    
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        vectorizer, svd, vectors, filenames = load_knowledge_base("./data/processed")
        print("Knowledge Base Loaded Successfully")
    
    except Exception as e:
        logger.error(f"An error occurred while loading the knowledge base: {str(e)}")
