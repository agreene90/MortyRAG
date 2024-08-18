import os
import sqlite3
from flask import Flask, request, jsonify
from controller import main as rag_main
from data_ingestion import load_documents, preprocess_documents
import pyttsx3  # Text-to-Speech (TTS) library

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
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Modify the query to match the database schema
        cursor.execute("SELECT filename, content FROM project_files WHERE content LIKE ?", ('%' + query + '%',))
        files = cursor.fetchall()
        
        conn.close()
        return files
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
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
        documents, filenames = load_documents(raw_folder_path)
        processed_docs = preprocess_documents(documents)
        retrieved_docs = [(filenames[i], processed_docs[i]) for i in range(len(processed_docs)) if query.lower() in processed_docs[i].lower()]
        return retrieved_docs
    except Exception as e:
        print(f"Error accessing raw files: {e}")
        return []

# Endpoint to generate a response from the RAG system
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400
    
    # Fetch relevant files from the database based on the query
    retrieved_docs = fetch_files_from_database(query)
    
    if not retrieved_docs:
        # If no relevant documents are found in the database, fallback to raw files
        retrieved_docs = fetch_files_from_raw(query)
        
        if not retrieved_docs:
            return jsonify({"error": "No relevant documents found"}), 404
    
    # Generate response using the RAG system
    response = rag_main(retrieved_docs)
    
    # Convert the response to speech
    tts_engine.say(response)
    tts_engine.runAndWait()
    
    return jsonify({"response": response})

# Entry point for Gunicorn
def create_app():
    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
