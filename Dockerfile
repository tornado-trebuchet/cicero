# syntax=docker/dockerfile:1

###########
# BUILDER #
###########
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps & clean up
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Poetry
RUN pip install --upgrade pip poetry

# Configure Poetry to use existing venv
RUN poetry config virtualenvs.create false

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies (excluding dev)
RUN poetry install --without dev --no-interaction --no-ansi

# Copy application code
COPY . .

############
# RUNTIME  #
############
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy virtual environment and application
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Runtime dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libpq5 \
 && rm -rf /var/lib/apt/lists/*

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]