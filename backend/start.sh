#!/bin/bash
set -e

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

echo "Starting uvicorn on port $PORT"

# Start uvicorn
exec uvicorn api:app --host 0.0.0.0 --port "$PORT" --log-level info
