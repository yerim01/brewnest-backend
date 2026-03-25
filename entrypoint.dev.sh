#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Loading fixtures..."
python manage.py loaddata store/fixtures/*.json || true

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000