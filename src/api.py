import os
import logging
import time
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
DEBUG = bool(int(os.getenv('DEBUG', 0)))  # DEBUG as an integer (0 or 1) for environment consistency

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

@app.before_request
def start_timer():
    """
    Start a timer before handling the request to measure response time.
    """
    request.start_time = time.time()

@app.after_request
def log_response(response):
    """
    Log the details of the response, including processing time.
    """
    response_time = time.time() - request.start_time
    logger.info(f"Request handled in {response_time:.4f} seconds with status {response.status_code}")
    return response

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
        # Validate content type
        if not request.is_json:
            logger.warning("Invalid content-type. Expected application/json.")
            return jsonify({"error": "Invalid content-type. Expected application/json."}), 415

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

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Handle cleanup of resources after the request context ends.
    """
    if exception:
        logger.error(f"Teardown exception: {str(exception)}")

if __name__ == "__main__":
    try:
        logger.info(f"Starting server at {HOST}:{PORT} with DEBUG={DEBUG}")
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except Exception as e:
        logger.error("Failed to start the server: %s", str(e))
        raise