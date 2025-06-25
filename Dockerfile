FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libffi-dev git && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

WORKDIR /app

# Copy dependency files and install dependencies only (no package install)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# Copy the rest of your code
COPY . .

# Install bash
RUN apt-get update && apt-get install -y bash

# Start a shell by default (or override in docker-compose or with `docker run`)
CMD ["/bin/bash"]