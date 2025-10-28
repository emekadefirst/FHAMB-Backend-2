# src/core/cache.py
import redis.asyncio as redis
import json
import logging
import asyncio
import enum
import datetime
import uuid
from typing import Optional, Any, Callable, Coroutine
from fastapi import Request
from functools import wraps
from tortoise.models import Model

logger = logging.getLogger(__name__)


def _json_default(obj):
    """Convert non-serializable objects to JSON-friendly formats."""
    from tortoise.models import Model  # ensure correct import

    if isinstance(obj, Model):
        # Convert Tortoise ORM model to dict
        return obj.__dict__  # includes _values and _meta info; or filter just your fields
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    # Fallback
    return str(obj)


class CachingService:
    _conn: Optional[redis.Redis] = None

    @classmethod
    async def open_conn(
        cls,
        host="redis",
        port=6379,
        db=0,
        max_connections=50,
        retries=5,
        delay=1,
    ):
        if cls._conn is None:
            for attempt in range(1, retries + 1):
                try:
                    cls._conn = redis.Redis(
                        host=host,
                        port=port,
                        db=db,
                        decode_responses=True,  # store strings
                        max_connections=max_connections,
                    )
                    await cls._conn.ping()
                    logger.info("Redis connection established")
                    return cls._conn
                except Exception as e:
                    logger.warning(f"Attempt {attempt}: Redis not ready yet ({e})")
                    cls._conn = None
                    await asyncio.sleep(delay)
            raise RuntimeError("Failed to connect to Redis after multiple attempts")

    @classmethod
    async def close_conn(cls):
        if cls._conn:
            await cls._conn.close()
            cls._conn = None
            logger.info("Redis connection closed")

    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 3600):
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")

        try:
            serialized = json.dumps(value, default=_json_default)
            await cls._conn.set(key, serialized, ex=ttl)
            logger.debug(f"Set key '{key}' in Redis (TTL={ttl}s)")
        except Exception as e:
            logger.error(f"Failed to set key '{key}' in Redis: {e}")
            raise

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")
        try:
            result = await cls._conn.get(key)
            if not result:
                return None
            return json.loads(result)
        except Exception as e:
            logger.error(f"Failed to get key '{key}' from Redis: {e}")
            raise

    @classmethod
    async def cache_or_fetch(
        cls,
        key: str,
        fetch_func: Callable[[], Coroutine[Any, Any, Any]],
        ttl: int = 3600,
    ) -> Any:
        cached = await cls.get(key)
        if cached is not None:
            logger.info(f"Cache hit for key '{key}'")
            return cached

        logger.info(f"Cache miss for key '{key}', fetching data...")
        data = await fetch_func()
        await cls.set(key, data, ttl)
        return data


def cache(ttl: int = 60):
    """Decorator for caching FastAPI endpoints."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to get the request from kwargs or args
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise ValueError("Request object not found for caching")

            key = f"cache:{request.url.path}?{request.url.query}"
            cached = await CachingService.get(key)
            if cached:
                return cached

            result = await func(*args, **kwargs)
            await CachingService.set(key, result, ttl)
            return result

        return wrapper
    return decorator
