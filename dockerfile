# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install dependencies and necessary tools for running Tkinter GUI in Docker
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port your app might run on
EXPOSE 5000

# Command to start Xvfb and run the application
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python3 main.py"]