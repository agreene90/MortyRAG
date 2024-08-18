# __init__.py

import logging
from .data_ingestion import load_documents, preprocess_documents, vectorize_documents
from .knowledge_base import save_knowledge_base, load_knowledge_base
from .retrieval import retrieve_documents
from .generation import ResponseGenerator

# Package metadata
__version__ = "1.0.0"
__author__ = "HermiTech LLC"
__license__ = "BSD 3-Clause License"

# Setup logging for the package
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Initializing {__name__} package, version {__version__}")

# Optional: Expose certain functionalities at the package level
__all__ = [
    "load_documents",
    "preprocess_documents",
    "vectorize_documents",
    "save_knowledge_base",
    "load_knowledge_base",
    "retrieve_documents",
    "ResponseGenerator"
]

# Package-wide configuration (if any)
DEFAULT_DATA_DIRECTORY = "./data/processed"
DEFAULT_MODEL_NAME = "t5-base"

logger.info("Package initialized successfully.")
