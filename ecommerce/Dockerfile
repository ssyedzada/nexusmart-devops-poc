# Use Python 3.12 slim image as base (Django 6.0+ requires Python 3.12+)
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Copy and set permissions for entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 for Django
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Run gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "ecommerce.wsgi:application"]