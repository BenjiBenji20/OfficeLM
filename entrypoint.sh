#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be reachable..."
until python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2); s.connect(('postgres', 5432)); s.close()" 2>/dev/null; do
  echo "PostgreSQL is not ready yet - waiting 1s..."
  sleep 1
done
echo "PostgreSQL port 5432 is open."

echo "Running Alembic database migrations..."
uv run --no-sync alembic upgrade head
echo "Alembic migrations completed successfully."

echo "Starting FastAPI server with Uvicorn..."
exec uv run --no-sync uvicorn main:app --host 0.0.0.0 --port 8000
