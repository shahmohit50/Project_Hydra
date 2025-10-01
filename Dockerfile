# Base Python environment
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy repo content
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
RUN git config --global --add safe.directory /app
RUN git config --global user.name "Hydra Bot" \
 && git config --global user.email "hydra@localhost"

# Expose port for FastAPI (optional)
EXPOSE 8000

# Default command to start orchestrator (can be overridden)
CMD ["python", "-m", "core.orchestrator"]
