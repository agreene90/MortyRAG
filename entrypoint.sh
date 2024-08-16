#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to initialize the database
initialize_database() {
    echo "Initializing the database..."
    python src/create_file_database.py
    echo "Database initialized successfully."
}

# Check if the database exists
DB_PATH="/app/data/files/resources/project_files.db"
if [ ! -f "$DB_PATH" ]; then
    echo "Database not found at $DB_PATH."
    initialize_database
else
    echo "Database found at $DB_PATH. Skipping initialization."
fi

# Default Gunicorn settings, can be overridden by environment variables
WORKERS=${GUNICORN_WORKERS:-3}
BIND_ADDRESS=${GUNICORN_BIND:-0.0.0.0:5000}

# Log the Gunicorn settings
echo "Starting Gunicorn with $WORKERS workers, binding to $BIND_ADDRESS..."

# Start the Gunicorn server with graceful shutdown handling
exec gunicorn --workers "$WORKERS" --bind "$BIND_ADDRESS" main:create_app
