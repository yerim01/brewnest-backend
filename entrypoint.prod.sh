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
if [ "${LOAD_FIXTURES:-false}" = "true" ]; then
    python manage.py loaddata store/fixtures/*.json
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput



# Create superuser if credentials provided
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "Creating superuser if not exists..."
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        "${DJANGO_SUPERUSER_USERNAME}",
        "${DJANGO_SUPERUSER_EMAIL}",
        "${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120
