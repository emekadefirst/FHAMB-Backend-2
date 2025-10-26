# Use uv-managed Python base image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS build

WORKDIR /app

# Optional: install netcat for health/wait scripts
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock README.md* ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable


# Copy the rest of the project
COPY . /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

# Run database migrations before starting app
CMD bash -c "\
    set -e && \
    echo '⏳ Waiting for database...' && \
    until nc -z db 5432; do sleep 1; done && \
    echo '✅ Database ready.' && \
    if PGPASSWORD='$DB_PASSWORD' psql -h db -U $DB_USER -d $DB_NAME -tAc \"SELECT 1 FROM information_schema.tables WHERE table_name='aerich';\" | grep -q 1; then \
        echo '🚀 Existing DB detected. Running migrations...' && \
        uv run makemigrations && \
        uv run migrate; \
    else \
        echo '⚡ Fresh DB detected. Recreating migrations...' && \
        rm -rf migrations/models && \
        uv run init && \
        uv run mount; \
    fi && \
    echo '🚀 Seeding database...' && \
    uv run seed && \
    echo '🚀 Starting app...' && \
    uv run prod"

