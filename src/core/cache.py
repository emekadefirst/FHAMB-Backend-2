# src/core/cache.py
import redis.asyncio as redis
import json
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)  

class CachingService:
    _conn: Optional[redis.Redis] = None

    @classmethod
    async def open_conn(cls, host="localhost", port=6379, db=0):
        if cls._conn is None:
            cls._conn = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                max_connections=10
            )
            try:
                await cls._conn.ping()
                logger.info("Redis connection established")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                cls._conn = None
        return cls._conn

    @classmethod
    async def close_conn(cls):
        if cls._conn:
            await cls._conn.close()
            cls._conn = None
            logger.info(" Redis connection closed")

    @classmethod
    async def set(cls, key: str, value: Dict):
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")
        try:
            await cls._conn.set(key, json.dumps(value))
            logger.debug(f"Set key '{key}' in Redis")
        except Exception as e:
            logger.error(f"Failed to set key '{key}' in Redis: {e}")
            raise

    @classmethod
    async def get(cls, key: str) -> Optional[Dict]:
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")
        try:
            result = await cls._conn.get(key)
            logger.debug(f"Retrieved key '{key}' from Redis")
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get key '{key}' from Redis: {e}")
            raise
