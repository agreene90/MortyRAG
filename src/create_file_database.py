import os
import sqlite3
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"Connected to SQLite database: {db_file}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {str(e)}")
        return None

def create_table(conn):
    """Create a table in the SQLite database to store project file information."""
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS project_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            filetype TEXT NOT NULL,
            filesize INTEGER NOT NULL,
            last_modified TEXT NOT NULL,
            content TEXT
        );
        """
        conn.execute(sql_create_table)
        logger.info("Project files table created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating table: {str(e)}")
        raise

def insert_file_data(conn, file_data):
    """Insert a new file record into the project_files table."""
    try:
        sql_insert = """
        INSERT INTO project_files(filename, filepath, filetype, filesize, last_modified, content)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        conn.execute(sql_insert, file_data)
        conn.commit()
        logger.info(f"Inserted file data into the database: {file_data[0]}")
    except sqlite3.Error as e:
        logger.error(f"Error inserting file data: {str(e)}")
        raise

def get_file_content(filepath, filetype):
    """Read and return the content of the file if it's a text-based file."""
    try:
        if filetype in ['.txt', '.md', '.py', '.json', '.csv']:  # Add more types as needed
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {str(e)}")
    return None

def scan_directory_and_populate_db(conn, directory):
    """Scan the directory and populate the database with file metadata and contents."""
    try:
        total_files = sum([len(files) for r, d, files in os.walk(directory)])
        processed_files = 0

        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                filetype = os.path.splitext(file)[1].lower()
                filesize = os.path.getsize(filepath)
                last_modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                content = get_file_content(filepath, filetype)
                file_data = (file, filepath, filetype, filesize, last_modified, content)
                
                insert_file_data(conn, file_data)
                
                processed_files += 1
                logger.info(f"Processed {processed_files}/{total_files} files")

    except Exception as e:
        logger.error(f"Error scanning directory and populating database: {str(e)}")
        raise

def initialize_database():
    """Initialize the database in the ./data/files/resources/ directory."""
    try:
        # Set up the database path in the ./data/files/resources/ directory
        database_directory = "./data/files/resources/"
        os.makedirs(database_directory, exist_ok=True)
        database_file = os.path.join(database_directory, "project_files.db")
        files_directory = "./data/files"

        # Create a database connection
        conn = create_connection(database_file)
        
        if conn:
            # Create project_files table
            create_table(conn)
            
            # Scan the files directory and populate the database
            scan_directory_and_populate_db(conn, files_directory)
            
            # Close the connection
            conn.close()
            logger.info("Database creation and population completed successfully.")
        else:
            logger.error("Failed to create database connection. Database initialization aborted.")
    except Exception as e:
        logger.error(f"An error occurred during database initialization: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_database()