FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Default port (can be overriden)
ENV PORT=8000

# Run the API
CMD ["python", "-m", "api.main"]