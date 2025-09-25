# 🚀 Fhamb-BE (Bank Backend)

This is the backend service built with **FastAPI + Tortoise ORM**, using **Aerich** for migrations and **Docker** for containerization.

---

## 📦 Project Setup

### 1️⃣ Database & Migrations

If you’re setting up the database for the first time:

```bash
# Initialize Aerich with your Tortoise config
aerich init -t src.core.database.TORTOISE_ORM

# Create initial schema
aerich init-db

# Seed the database with sample data
uv run scripts/seeds.py
```

For schema changes:

```bash
# Create new migrations
uv run makemigrations

# Apply migrations
uv run migrate
```

---

### 2️⃣ Clean Python Cache (optional)

```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## 🐳 Running with Docker

### Build & Run (Dev)

```bash
docker compose -f dev-docker-compose.yml up -d --build
```

### Build & Run (Prod)

```bash
# Build image
docker build -t fhamb-be .

# Run container
docker run -p 80:80 fhamb-be
```

### Logs

```bash
docker logs -f fhamb-be
```

### Stop containers

```bash
docker compose down

# or for dev only
docker compose -f dev-docker-compose.yml down
```

---

## 🌐 Accessing the App

Once running, open in your browser:

👉 [http://localhost:8000](http://localhost:8000)

---

## 🔑 SSH Keys (for deploys)

Generate deploy key:

```bash
ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/deploy-key -N ""
```

---

## ⚡ Alternative Docker Commands with `.env`

```bash
docker compose --env-file .env -f dev-docker-compose.yml up -d --build
```

---

## 🛠️ Workflow Summary

* `uv run makemigrations` → Create schema migrations
* `uv run migrate` → Apply migrations
* `docker compose ...` → Build & run containers
* `docker logs -f fhamb-be` → Monitor logs

---
