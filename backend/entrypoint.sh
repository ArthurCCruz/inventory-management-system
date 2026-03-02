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

# Create superuser if not exists
echo "Creating superuser if not exists..."
python manage.py create_superuser_if_not_exists

# Create demo data
echo "Creating demo data..."
python manage.py create_demo_data

# Collect static files in production
if [ "$DEBUG" = "False" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

echo "Starting application..."
exec "$@"
