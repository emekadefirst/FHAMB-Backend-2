#!/bin/bash
set -e

echo "🔍 Checking for Aerich migrations..."

# Make sure we're in the correct working directory
cd "$(dirname "$0")"

# Ensure Tortoise config path exists
TORTOISE_CONFIG="src.core.database.TORTOISE_ORM"

if [ -d "./migrations" ]; then
    echo "📦 Running Aerich upgrade..."
    uv run aerich migrate || echo "No new migrations found."
    uv run aerich upgrade
else
    echo "🧩 Initializing Aerich..."
    uv run aerich init -t $TORTOISE_CONFIG
    uv run aerich init-db
fi

echo "🌱 Running seed..."
uv run seed || echo "⚠️ No seed script found or it failed."

echo "🚀 Starting server..."
exec "$@"

