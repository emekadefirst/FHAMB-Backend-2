FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

COPY . /app


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

EXPOSE 8080

CMD ["uv", "run", "prod"]
