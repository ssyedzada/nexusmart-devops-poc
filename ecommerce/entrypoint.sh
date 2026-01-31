#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# Wait for database to be ready (optional, docker-compose handles this with healthcheck)
sleep 2

echo "Running migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed, continuing..."

echo "Starting application..."
exec "$@"

