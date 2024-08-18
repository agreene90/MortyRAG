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
    This ensures the model is loaded into memory once and reused for subsequent requests.
    """
    try:
        logger.info("Loading model and data for the first time...")
        model_cache['vectorizer'], model_cache['svd'], model_cache['vectors'], model_cache['filenames'] = rag_main.load_cached_model("./data/processed")
        logger.info("Model and data loaded successfully.")
    except Exception as e:
        logger.error("Error loading model and data: %s", str(e))
        raise RuntimeError("Failed to load model and data.") from e

@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate a response from the RAG system.
    
    The endpoint expects a JSON payload with the following structure:
    {
        "query": "Your query here"
    }
    
    Returns:
    - JSON response with the generated text based on the query.
    """
    try:
        # Extract the query from the POST request
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            logger.warning("No query provided in the request.")
            return jsonify({"error": "Query not provided"}), 400
        
        # Process the query using the RAG system
        logger.info(f"Processing query: '{query}'")
        response = rag_main(query, model_cache)
        
        logger.info("Query processed successfully, returning response.")
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error("Error processing query: %s", str(e))
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    try:
        logger.info(f"Starting server at {HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except Exception as e:
        logger.error("Failed to start the server: %s", str(e))
        raise
