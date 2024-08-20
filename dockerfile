# Stage 1: Build environment
FROM python:3.10 as build-env

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies (including transformers and other heavy packages)
RUN pip install --no-cache-dir -r requirements.txt

# Download and cache necessary Hugging Face models
RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; T5Tokenizer.from_pretrained('t5-base'); T5ForConditionalGeneration.from_pretrained('t5-base')"

# Copy the rest of the application code
COPY . .

# Clean up unnecessary files
RUN rm -rf /root/.cache/pip

# Stage 2: Final image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the dependencies and installed packages from the build environment
COPY --from=build-env /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=build-env /app /app

# Command to run the application
CMD ["python", "main.py"]