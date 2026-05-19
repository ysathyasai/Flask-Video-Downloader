# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies, including ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Render expects (10000)
EXPOSE 10000

# Run the application using Gunicorn binding to port 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

