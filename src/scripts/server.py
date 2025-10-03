import uvicorn
from src.config.env import CORS_ALLOWED_ORIGINS
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from src.core.database import TORTOISE_ORM
from src.core.routes import routes

from contextlib import asynccontextmanager
from src.logs.logger import JSONFormatter
from src.dependencies.middlewares.logmiddleware import LoggingMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import logging

logging.getLogger("tortoise").setLevel(logging.CRITICAL)

root_logger = logging.getLogger()
for h in root_logger.handlers[:]:
    root_logger.removeHandler(h)

file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setFormatter(JSONFormatter())
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.INFO)


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
    default_response_class=responses.ORJSONResponse,
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
allowed_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5500", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://fhamortgage.gov.ng"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)


list(map(lambda r: app.include_router(r), routes))



def run_server():
    uvicorn.run("src.scripts.server:app", host="0.0.0.0", port=8080, reload=True)


def run_prod():
    uvicorn.run("src.scripts.server:app", host="0.0.0.0", port=8080, reload=False, workers=2)

