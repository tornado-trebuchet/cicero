#!/bin/bash

# Start PostgreSQL database using docker-compose
docker compose up -d postgres

# Wait for the database to be ready
echo "Waiting for PostgreSQL to start..."
sleep 5

# Run FastAPI app with uvicorn
uvicorn src.interface.api.main:app --host 0.0.0.0 --port 8000