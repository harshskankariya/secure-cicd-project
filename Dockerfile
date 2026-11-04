FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Update Linux packages and remove unnecessary package lists
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Configure Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd --create-home appuser

# Copy application files
COPY --chown=appuser:appuser . .

# Run application as non-root user
USER appuser

# Application port
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]