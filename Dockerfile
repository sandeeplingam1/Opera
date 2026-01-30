# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY opera/ ./opera/
COPY .env.example .env

# Create data directories
RUN mkdir -p /data/chroma_db

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "opera.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
