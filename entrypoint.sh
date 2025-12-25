#!/bin/bash
set -e

echo "=== Setting up Django ==="

# Создаем папку для статики если нет
mkdir -p staticfiles

echo "1. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "2. Applying database migrations..."
python manage.py migrate --noinput

echo "3. Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
