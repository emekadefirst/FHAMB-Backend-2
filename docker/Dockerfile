# Use uv-managed Python base image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS build

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock README.md* ./

# Install dependencies (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Copy the rest of the app
COPY . /app

# Set PATH for .venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

# Run production server
CMD ["uv", "run", "prod"]
