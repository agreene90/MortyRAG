import os
import logging
from flask import Flask, request, jsonify
from controller import main as rag_main

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables for configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = bool(os.getenv('DEBUG', False))

# Cache for the model and vectorizer (if needed)
model_cache = {
    'vectorizer': None,
    'svd': None,
    'vectors': None,
    'filenames': None
}

@app.before_first_request
def load_model():
    """
    Load the model and other necessary components before the first request.
    """
    try:
        logger.info("Loading model and data...")
        vectorizer, svd, vectors, filenames = rag_main.load_knowledge_base("./data/processed")
        model_cache['vectorizer'] = vectorizer
        model_cache['svd'] = svd
        model_cache['vectors'] = vectors
        model_cache['filenames'] = filenames
        logger.info("Model and data loaded successfully.")
    except Exception as e:
        logger.error("Error loading model and data: %s", str(e))
        raise RuntimeError("Failed to load model and data.") from e

@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate a response from the RAG system.
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            logger.warning("Query not provided in request.")
            return jsonify({"error": "Query not provided"}), 400
        
        # Generate the response using the RAG system
        response = rag_main(query, model_cache)
        
        logger.info("Query processed successfully.")
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error("Error processing query: %s", str(e))
        return jsonify({"error": "An error occurred processing your request."}), 500

if __name__ == "__main__":
    logger.info(f"Starting server at {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
