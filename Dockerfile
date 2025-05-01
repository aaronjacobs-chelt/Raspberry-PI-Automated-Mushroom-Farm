# Development environment for MycoMonitor
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash developer

# Set up development directory
WORKDIR /app
COPY requirements*.txt ./

# Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements-dev.txt

# Mock RPi.GPIO for development
RUN python -m pip install fake-rpi

# Copy project files
COPY . .

# Install the package in development mode
RUN pip install -e .

# Switch to non-root user
USER developer

# Command to run tests
CMD ["pytest"]
