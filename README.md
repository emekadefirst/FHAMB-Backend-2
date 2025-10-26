
# 🚀 FHAMB Backend

A high-performance asynchronous backend built with **FastAPI**, **Tortoise ORM**, **Redis**, and **PostgreSQL**.  
It uses **uv** as a Python package manager and supports both **local** and **Dockerized** environments.

---

## 🌀 Clone the Project

```bash
git clone https://github.com/your-username/fhamb-be.git
cd fhamb-be
````

---

# 🧩 Install uv

### For macOS or Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### For Windows (run PowerShell as Administrator)

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## ⚙️ Run Without Docker

Install dependencies:

```bash
uv sync --frozen
```

### Activate virtual environment

For **Windows CMD**:

```
.venv\Scripts\activate
```

For **Linux or macOS**:

```
source .venv/bin/activate
```

For **Windows Bash terminal**:

```
source .venv/Scripts/activate
```

---

## 🔐 Environment Setup

Make sure your `.env` file is available in the project root.
You can duplicate the sample file using:

```bash
cp .env.sample .env
```

---

## 🧱 Database Migration & Initialization

If the `migrations/` folder **does not exist**, run:

```bash
aerich init -t src.core.database.TORTOISE_ORM
aerich init-db
```

Else (if migrations exist and you’ve made changes), run:

```bash
uv run makemigrations
uv run migrate
```

Then seed your data:

```bash
uv run seed
```

---

## ▶️ Run the Development Server

```bash
uv run dev
```

Server runs by default on:

```
http://127.0.0.1:8000
```

---

## 🐳 Run with Docker

Docker files and compose files are located inside `src/docker`.

```
ls src/docker
```

Expected structure:

```
src/
│
├── docker/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── docker-compose.yml          # app only
│   ├── docker-compose.db.yml       # postgres
│   ├── docker-compose.redis.yml    # redis
│
├── .env
├── .env.prod
├── .env.sample
```

---

## 🧱 Build & Run All Containers

Run app, PostgreSQL, and Redis together:

```bash
cd src/docker
docker compose -f docker/docker-compose.yml -f docker/docker-compose.db.yml -f docker/docker-compose.redis.yml up --build
```

---

## 🧩 Run Individual Containers

### Run only the database

```bash
docker compose -f docker-compose.db.yml up -d
```

### Run only Redis

```bash
docker compose -f docker-compose.redis.yml up -d
```

### Run only the app

```bash
docker compose -f docker-compose.yml up --build
```

---

## 📜 View Logs

### All logs (app + db + redis)

```bash
docker compose -f docker-compose.yml -f docker-compose.db.yml -f docker-compose.redis.yml logs -f
```
```
docker network create fhamb_net
```
### Individual service logs

```bash
docker compose -f docker-compose.yml logs -f app
docker compose -f docker-compose.db.yml logs -f db
docker compose -f docker-compose.redis.yml logs -f redis
```

---

## 🛑 Stop Containers

### Stop all containers

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.db.yml -f docker/docker-compose.redis.yml down
```

### Stop and remove containers + volumes

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.db.yml -f docker/docker-compose.redis.yml down --volumes
```

---

## 🧹 Clean Builds

Rebuild all images (fresh, no cache):

```bash
docker compose  --env-file .env.prod -f docker/docker-compose.yml -f docker/docker-compose.db.yml -f docker/docker-compose.redis.yml build --no-cache
```

---

## 🧰 Useful Docker Commands

### View running containers

```bash
docker ps
```

### Stop all running containers

```bash
docker stop $(docker ps -q)
```

### Remove stopped containers

```bash
docker container prune
```

### Remove unused volumes

```bash
docker volume prune
```

---

## 📘 Project Directory Structure

```
.github/
src/
│
├── apps/
├── core/
├── logs/
├── enums/
├── error/
├── scripts/
├── config/
├── dependencies/
├── libs/
├── utilities/
├── docker/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── docker-compose.yml
│   ├── docker-compose.db.yml
│   ├── docker-compose.redis.yml
│
├── .env
├── .env.prod
├── .env.sample
```

---

## 🧠 Quick Summary

* `uv` manages dependencies (fast replacement for pip)
* `aerich` handles migrations (`makemigrations`, `migrate`)
* `seed` populates initial data
* `docker-compose.*.yml` files manage app, DB, and Redis
* Run everything together with:

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.db.yml -f docker-compose.redis.yml up --build
  ```

---

✅ **Now you’re ready to develop, migrate, and deploy FHAMB Backend confidently — locally or in Docker.**

```

---

Would you like me to generate a **matching `Makefile`** (so you can just run `make up`, `make logs`, `make down`, etc.) to go along with this README?
```
