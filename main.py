import os
import sqlite3
from flask import Flask, request, jsonify
from controller import main as rag_main
from data_ingestion import load_documents, preprocess_documents
import pyttsx3  # Text-to-Speech (TTS) library
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()

# Define paths to important directories
base_dir = os.path.dirname(os.path.abspath(__file__))
files_folder_path = os.path.join(base_dir, 'data', 'files')
raw_folder_path = os.path.join(base_dir, 'data', 'raw')
database_path = os.path.join(files_folder_path, 'resources', 'project_files.db')

def fetch_files_from_database(query):
    """
    Fetch files from the SQLite database based on a query.

    Args:
    - query (str): The search query to filter files in the database.

    Returns:
    - List of tuples containing file metadata and content.
    """
    try:
        logger.info(f"Fetching files from the database for query: '{query}'")
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Sanitized query to prevent SQL injection
        sanitized_query = f"%{query.replace('%', '%%')}%"
        cursor.execute("SELECT filename, content FROM project_files WHERE content LIKE ?", (sanitized_query,))
        files = cursor.fetchall()

        conn.close()
        logger.info(f"Retrieved {len(files)} files from the database.")
        return files
    except sqlite3.Error as e:
        logger.error(f"Error accessing database: {e}")
        return []

def fetch_files_from_raw(query):
    """
    Fetch files from the raw text directory if no database entries are found.

    Args:
    - query (str): The search query to filter files in the raw folder.

    Returns:
    - List of tuples containing file metadata and content.
    """
    try:
        logger.info(f"Fetching files from the raw directory for query: '{query}'")
        documents, filenames = load_documents(raw_folder_path)
        processed_docs = preprocess_documents(documents)
        retrieved_docs = [(filenames[i], processed_docs[i]) for i in range(len(processed_docs)) if query.lower() in processed_docs[i].lower()]
        logger.info(f"Retrieved {len(retrieved_docs)} files from the raw directory.")
        return retrieved_docs
    except Exception as e:
        logger.error(f"Error accessing raw files: {e}")
        return []

@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate a response from the RAG system.
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            logger.warning("No query provided in the request.")
            return jsonify({"error": "Query not provided"}), 400

        query = data['query'].strip()

        if not query:
            logger.warning("Received an empty query.")
            return jsonify({"error": "Query cannot be empty"}), 400

        # Fetch relevant files from the database based on the query
        retrieved_docs = fetch_files_from_database(query)

        if not retrieved_docs:
            # If no relevant documents are found in the database, fallback to raw files
            retrieved_docs = fetch_files_from_raw(query)

            if not retrieved_docs:
                logger.warning("No relevant documents found for the query.")
                return jsonify({"error": "No relevant documents found"}), 404

        # Generate response using the RAG system
        logger.info("Generating response using the RAG system...")
        response = rag_main(query, {'vectorizer': None, 'svd': None, 'vectors': None, 'filenames': retrieved_docs})

        # Convert the response to speech
        logger.info("Converting generated response to speech.")
        tts_engine.say(response)
        tts_engine.runAndWait()

        logger.info("Response generated and sent successfully.")
        return jsonify({"response": response})

    except Exception as e:
        logger.error(f"An error occurred while processing the request: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

def create_app():
    """
    Create and return the Flask app instance.
    """
    return app

if __name__ == "__main__":
    try:
        logger.info("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start Flask server: {str(e)}")