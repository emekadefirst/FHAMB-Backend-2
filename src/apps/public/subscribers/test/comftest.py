# tests/conftest.py
import pytest
from tortoise import Tortoise
from src.core.database import TEST_TORTOISE_ORM   # Use your ORM config

@pytest.fixture(scope="module", autouse=True)
async def init_db():
    """
    Initialize the Tortoise ORM before tests and close after.
    """
    await Tortoise.init(config=TEST_TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
