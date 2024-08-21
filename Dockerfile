FROM python:3.10-slim

# Install necessary system dependencies for Tkinter, OCR, and handling various file types
RUN apt-get update && apt-get install -y \
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
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install Python dependencies, handling any issues with demjson
RUN pip install --no-cache-dir simplejson \
    && sed -i 's/use_2to3=True,//g' setup.py \
    && pip install --no-cache-dir -r requirements.txt

# Expose the display port for GUI applications
ENV DISPLAY=:0

# Run the Tkinter application
CMD ["python", "main.py"]