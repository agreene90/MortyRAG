# Use the official PyTorch image as the base image
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run your application with Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "main:create_app"]
