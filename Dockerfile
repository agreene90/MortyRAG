# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure that the Tkinter app uses the host's display
ENV DISPLAY=:0

# Expose the port for forwarding if necessary (you can remove this if not needed)
EXPOSE 8081

# Run the main application (Tkinter app)
CMD ["python", "main.py"]
