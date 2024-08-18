import os
import pickle
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_knowledge_base(vectorizer, svd, vectors, filenames, filepath, version="v1"):
    """
    Save the components of the knowledge base to the specified filepath.
    
    Parameters:
    - vectorizer: The vectorizer used to transform documents.
    - svd: The SVD model used for dimensionality reduction.
    - vectors: The matrix of reduced document vectors.
    - filenames: List of filenames corresponding to the document vectors.
    - filepath: The directory where the knowledge base components will be saved.
    - version: Version string to append to saved files (default is "v1").
    """
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            logger.info(f"Created directory: {filepath}")

        logger.info(f"Saving vectorizer (version: {version})...")
        with open(os.path.join(filepath, f'vectorizer_{version}.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)
            
        logger.info(f"Saving SVD model (version: {version})...")
        with open(os.path.join(filepath, f'svd_{version}.pkl'), 'wb') as f:
            pickle.dump(svd, f)
        
        logger.info(f"Saving reduced document vectors (version: {version})...")
        np.save(os.path.join(filepath, f'reduced_vectors_{version}.npy'), vectors)
        
        logger.info(f"Saving filenames list (version: {version})...")
        np.save(os.path.join(filepath, f'filenames_{version}.npy'), filenames)
        
        logger.info("Knowledge base saved successfully.")
    
    except Exception as e:
        logger.error(f"Error saving knowledge base: {str(e)}")
        raise

def load_knowledge_base(filepath, version="v1"):
    """
    Load the components of the knowledge base from the specified filepath.
    
    Parameters:
    - filepath: The directory where the knowledge base components are stored.
    - version: Version string to append to file names during loading (default is "v1").
    
    Returns:
    - vectorizer: The loaded vectorizer.
    - svd: The loaded SVD model.
    - vectors: The loaded matrix of reduced document vectors.
    - filenames: The loaded list of filenames.
    """
    try:
        logger.info(f"Loading vectorizer (version: {version})...")
        with open(os.path.join(filepath, f'vectorizer_{version}.pkl'), 'rb') as f:
            vectorizer = pickle.load(f)
            
        logger.info(f"Loading SVD model (version: {version})...")
        with open(os.path.join(filepath, f'svd_{version}.pkl'), 'rb') as f:
            svd = pickle.load(f)
        
        logger.info(f"Loading reduced document vectors (version: {version})...")
        vectors = np.load(os.path.join(filepath, f'reduced_vectors_{version}.npy'))
        
        logger.info(f"Loading filenames list (version: {version})...")
        filenames = np.load(os.path.join(filepath, f'filenames_{version}.npy'))
        
        logger.info("Knowledge base loaded successfully.")
        
        # Validate the loaded components
        if not isinstance(vectorizer, type(vectorizer)):
            raise ValueError("Loaded vectorizer is not of the correct type.")
        if not isinstance(svd, type(svd)):
            raise ValueError("Loaded SVD model is not of the correct type.")
        if vectors.shape[0] != len(filenames):
            raise ValueError("Mismatch between the number of vectors and filenames.")
        
        return vectorizer, svd, vectors, filenames
    
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found during knowledge base loading: {str(fnf_error)}")
        raise
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Example version to load
        version_to_load = "v1"
        vectorizer, svd, vectors, filenames = load_knowledge_base("./data/processed", version=version_to_load)
        logger.info("Knowledge Base Loaded Successfully")
    
    except Exception as e:
        logger.error(f"An error occurred while loading the knowledge base: {str(e)}")
