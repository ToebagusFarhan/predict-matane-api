# Use an official lightweight Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Create and set the working directory
WORKDIR /app

# Install system dependencies required for bcrypt and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt to leverage Docker caching
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the required port
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "server:app"]
