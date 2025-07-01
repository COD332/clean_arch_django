# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# System deps for psycopg2 and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the poetry files first (for caching)
COPY ./project/pyproject.toml ./project/poetry.lock ./

# Install dependencies in virtualenv-less mode
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy only the project folder contents to /app (this will merge with existing files)
COPY ./project/ ./

# Expose port
EXPOSE 8000

# Default run command  
CMD ["gunicorn", "clean_arch_project.wsgi:application", "--bind", "0.0.0.0:8000"]
