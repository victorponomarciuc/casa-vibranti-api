#!/usr/bin/env bash
set -e

# Ensure runtime dirs exist
mkdir -p /app/runtime /app/media /app/static

# DB wait (optional but useful)
if [ -n "${DB_PSQL_HOST:-}" ]; then
  echo "Waiting for DB at ${DB_PSQL_HOST}:${DB_PSQL_PORT:-5432}..."
  for i in $(seq 1 60); do
    (echo > /dev/tcp/${DB_PSQL_HOST}/${DB_PSQL_PORT:-5432}) >/dev/null 2>&1 && break
    sleep 1
  done
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput || true

echo "Starting app..."
# If you have ASGI (Django Channels), replace wsgi with asgi and use uvicorn workers.
# Default: WSGI
exec gunicorn backend.wsgi:application \
  --bind 0.0.0.0:8123 \
  --workers 3 \
  --timeout 120
