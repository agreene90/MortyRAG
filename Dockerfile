# Use the official PyTorch image as the base image
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent storage of the database
VOLUME ["/app/data/files/resources/"]

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Health check to ensure the API is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]
