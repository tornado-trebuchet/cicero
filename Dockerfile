# syntax=docker/dockerfile:1

###########
# BUILDER #
###########
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps & clean up in one layer
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy project metadata and lockfile
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies (exclude dev)
RUN pip install --upgrade pip poetry \
 && poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi \
 && find / -name uvicorn || true

# Copy the rest of application code
COPY . .

############
# RUNTIME  #
############
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy dependencies and application code from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Default command
CMD ["python3"]
