#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

echo "Starting production entrypoint..."

# Optional: wait for database to be ready
echo "Waiting for database..."
until python -c "import django; from django.db import connections; connections['default'].cursor()" 2>/dev/null; do
  echo "Database unavailable, retrying in 2s..."
  sleep 2
done
echo "Database is ready!"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Load fixtures
echo "Loading fixtures..."
python manage.py loaddata store/fixtures/*.json

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput



# Create superuser if credentials provided
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "Creating superuser if not exists..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists"
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120
