#!/bin/bash
set -e

echo "🔍 Checking for Aerich migrations..."

if [ -d "./migrations" ]; then
    echo "📦 Running Aerich upgrade..."
    uv run aerich upgrade || echo "⚠️ Aerich upgrade failed"
else
    echo "🧩 Initializing Aerich..."
    uv run aerich init -t src.core.database.TORTOISE_ORM
    uv run aerich init-db
fi

echo "🌱 Running seed..."
uv run seed  # no quotes, do NOT use exec here

echo "🚀 Starting server..."
exec "$@"
