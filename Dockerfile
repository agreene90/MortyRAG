# Use the official Python slim image
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy all application files to the container
COPY . /app

# Install Python dependencies including transformers, PyTorch, TensorFlow, Flax, and PyPDF2
RUN pip install --no-cache-dir torch \
    tensorflow \
    flax \
    transformers \
    PyPDF2 \
    simplejson \
    demjson \
    && pip install --no-cache-dir -r requirements.txt

# Expose the display port for GUI applications
ENV DISPLAY=:0

# Set the entrypoint to the Tkinter application
CMD ["python", "main.py"]
