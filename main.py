import os
from flask import Flask, request, jsonify
from controller import main as rag_main
import pyttsx3  # Text-to-Speech (TTS) library

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()

# Define paths to important directories
base_dir = os.path.dirname(os.path.abspath(__file__))
files_folder_path = os.path.join(base_dir, 'files')
raw_folder_path = os.path.join(base_dir, 'data', 'raw')

# Endpoint to generate a response from the RAG system
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400
    
    response = rag_main(query)
    
    # Convert the response to speech
    tts_engine.say(response)
    tts_engine.runAndWait()
    
    return jsonify({"response": response})

# Entry point for gunicorn
def create_app():
    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
