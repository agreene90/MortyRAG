from flask import Flask, request, jsonify
from controller import main as rag_main

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400
    
    response = rag_main(query)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # This line is typically bypassed when using gunicorn
