#!/bin/bash
set -e

echo "🔍 Checking for Aerich migrations..."

# Make sure we're in the correct working directory
cd "$(dirname "$0")"

# Ensure Tortoise config path exists
TORTOISE_CONFIG="src.core.database.TORTOISE_ORM"

# Check if migrations folder exists and has migration files
if [ -d "./migrations/models" ] && [ "$(ls -A ./migrations/models 2>/dev/null)" ]; then
    echo "📦 Running Aerich upgrade..."
    uv run aerich migrate || echo "⚠️ No new migrations found."
    uv run aerich upgrade
else
    echo "🧩 No migrations found. Initializing Aerich..."
    uv run aerich init-db
fi

echo "🌱 Running seed..."
if uv run seed; then
    echo "✅ Seeding complete."
else
    echo "⚠️ No seed script found or seeding failed."
fi

echo "🚀 Starting server..."
exec "$@"
