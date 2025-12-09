#!/bin/bash
set -e

# Railway will map whatever port we use internally to their external port
# We'll use 8000 internally and let Railway handle the external mapping
PORT=8000

echo "Starting uvicorn on port $PORT"

# Start uvicorn
exec uvicorn api:app --host 0.0.0.0 --port $PORT --log-level info
