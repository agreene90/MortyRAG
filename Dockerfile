# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Install necessary system dependencies for Tkinter, OCR, and handling various file types
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    tesseract-ocr \
    poppler-utils \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    ghostscript \
    unzip \
    sqlite3 && rm -rf /var/lib/apt/lists/*  # Remove apt lists after installation

# Set the working directory
WORKDIR /app

# Copy all application files to the container
COPY . .

# Upgrade pip and install Python dependencies including bs4, lxml, and scikit-learn
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir beautifulsoup4 lxml scikit-learn

# Set environment variable to suppress Python bytecode (.pyc) generation
ENV PYTHONDONTWRITEBYTECODE=1

# Set environment variable to buffer output, useful for logging
ENV PYTHONUNBUFFERED=1

# Expose the display port for GUI applications
ENV DISPLAY=:0

# Create a directory for the SQLite database
RUN mkdir -p /app/database

# Set up a non-root user for security purposes
RUN useradd -m myuser \
    && chown -R myuser:myuser /app
USER myuser

# Define a volume to persist the database file outside of the container
VOLUME ["/app/database"]

# Set the SQLite database path in an environment variable
ENV SQLITE_DB_PATH=/app/database/mortrag.db

# Run the Tkinter application
CMD ["python", "main.py"]