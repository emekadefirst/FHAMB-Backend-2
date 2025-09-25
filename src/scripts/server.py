import uvicorn
from src.config.env import CORS_ALLOWED_ORIGINS
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from src.core.database import TORTOISE_ORM
from src.core.routes import routes
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from src.dependencies.middlewares.logmiddleware import LoggingMiddleware
from fastapi.middleware.gzip import GZipMiddleware


@asynccontextmanager
async def redisconn(app: FastAPI):
    redis = await aioredis.from_url("redis://localhost:6379")
    app.state.redis = redis
    yield
    await redis.close()

app = FastAPI(
    title="FHA Mortgage Bank API documentation",
    description="This is the API documentation for the FHA Mortgage Bank solely for acknowledged developers.",
    version="1.0.0",
    contact={
        "name": "FHA Mortgage Bank",
        "url": "https://www.fhamortgagebank.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/"
    },
    openapi_tags=[
        {
            "name": "FHA Mortgage Bank",
            "description": "API for FHA Mortgage Bank"
        }
    ],
    lifespan=redisconn,
    default_response_class=responses.ORJSONResponse,
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)


list(map(lambda r: app.include_router(r), routes))



def run_server():
    uvicorn.run("src.scripts.server:app", host="0.0.0.0", port=8080, reload=True)
