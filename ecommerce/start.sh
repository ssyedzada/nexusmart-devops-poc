#!/bin/bash
set -e

echo "Starting application on Render..."

# Run migrations (in case they weren't run during build)
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations already applied"

# Start Gunicorn with Render's PORT environment variable
echo "Starting Gunicorn on port $PORT..."
exec gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120

