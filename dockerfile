# Stage 1: Build environment
FROM python:3.10 AS build-env

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install SentencePiece
RUN pip install sentencepiece

# Download and cache necessary Hugging Face models
RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; \
    T5Tokenizer.from_pretrained('t5-base'); \
    T5ForConditionalGeneration.from_pretrained('t5-base')"

# Copy the rest of the application code
COPY . .

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build-env /app /app

# Set the entry point
CMD ["python", "main.py"]
