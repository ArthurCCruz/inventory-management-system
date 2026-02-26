#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - continuing..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files in production
if [ "$DEBUG" = "False" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

echo "Starting application..."
exec "$@"
