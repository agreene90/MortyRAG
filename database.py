import os
import sqlite3
from pathlib import Path
from retriever import read_local_file
from sklearn.feature_extraction.text import TfidfVectorizer

# Get the database path from the environment variable
DB_PATH = os.getenv("SQLITE_DB_PATH", "./mortrag.db")
RAW_DATA_DIR = Path('./data/raw/')

def initialize_db():
    """Initialize the SQLite database and create necessary tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY,
                query TEXT NOT NULL,
                file_path TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY,
                model_version TEXT NOT NULL,
                saved_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL UNIQUE,
                content TEXT,
                vector BLOB,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_query(query: str, file_path: str, result: str):
    """Save the query and result to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO queries (query, file_path, result)
            VALUES (?, ?, ?)
        """, (query, file_path, result))
        conn.commit()

def get_query_history():
    """Retrieve all query history from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM queries ORDER BY timestamp DESC")
        return cursor.fetchall()

def save_model_version(model_version: str):
    """Save the model version to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO models (model_version)
            VALUES (?)
        """, (model_version,))
        conn.commit()

def get_model_versions():
    """Retrieve all saved model versions from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models ORDER BY saved_at DESC")
        return cursor.fetchall()

def tokenize_and_vectorize(text):
    """Tokenize and create a vector representation of the text using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english')
    vector = vectorizer.fit_transform([text]).toarray()[0]
    return vector

def load_files_to_db():
    """Load all supported files from /data/raw/ into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Process each supported file type in the /data/raw/ directory
        for file_path in RAW_DATA_DIR.glob('*.txt'):
            content = read_local_file(file_path)
            vector = tokenize_and_vectorize(content)
            
            # Check if the document is already in the database
            cursor.execute("""
                SELECT COUNT(*) FROM documents WHERE filename = ?
            """, (file_path.name,))
            exists = cursor.fetchone()[0]

            if exists:
                # Update the content if it already exists
                cursor.execute("""
                    UPDATE documents
                    SET content = ?, vector = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE filename = ?
                """, (content, vector, file_path.name))
            else:
                # Insert new content
                cursor.execute("""
                    INSERT INTO documents (filename, content, vector)
                    VALUES (?, ?, ?)
                """, (file_path.name, content, vector))
        
        conn.commit()

def get_document_content(filename: str):
    """Retrieve content of a specific document from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT content FROM documents WHERE filename = ?
        """, (filename,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_document_vector(filename: str):
    """Retrieve vector of a specific document from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vector FROM documents WHERE filename = ?
        """, (filename,))
        result = cursor.fetchone()
        return result[0] if result else None