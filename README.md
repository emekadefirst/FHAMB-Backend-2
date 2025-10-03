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

### Logs

```bash
docker logs -f id
```

### Stop containers

```bash
docker compose down

```



## 🌐 Accessing the App

Once running, open in your browser:

👉 [http://localhost:8000](http://localhost:8000)


## 🔑 SSH Keys (for deploys)

Generate deploy key:

```bash
ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/deploy-key -N ""
```

---

## ⚡ Alternative Docker Commands with `.env`

```bash

docker compose --env-file .env -f docker/docker-compose.yml up -d --build
docker compose -f docker/docker-compose.yml down

```

---

## 🛠️ Workflow Summary

* `uv run makemigrations` → Create schema migrations
* `uv run migrate` → Apply migrations
* `docker compose ...` → Build & run containers
* `docker logs -f fhamb-be` → Monitor logs


`sudo certbot certonly --nginx -d api.fhamortgage.gov.ng
`

---
