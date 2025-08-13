#!/bin/bash

# Start PostgreSQL database using docker-compose
docker compose up -d postgres

# Run FastAPI app with uvicorn
uvicorn backend.interface.api.main:app --host 0.0.0.0 --port 8000 --reload

# Run angular fromtend 
npx --prefix frontend ng serve --proxy-config proxy.conf.json --project cicero_client --configuration=development