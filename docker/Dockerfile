
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Install required utilities
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Ensure Python path points to venv
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md* ./

# Install deps (aerich included)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Fix potential aerich permission issues
RUN chmod +x /app/.venv/bin/aerich || true

# Copy source after dependencies
COPY . /app

EXPOSE 8080

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
        uv run aerich init -t src.core.database.TORTOISE_ORM && \
        uv run aerich init-db; \
    fi && \
    echo '🚀 Seeding database...' && \
    uv run seed && \
    echo '🚀 Starting app...' && \
    uv run prod"
