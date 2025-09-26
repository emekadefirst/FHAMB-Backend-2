# tests/test_subscriber.py
import pytest
from src.apps.public.subscribers.services import SubscriberService
from src.apps.public.subscribers.schemas import SubscriberSchema

@pytest.mark.asyncio
async def test_create_subscriber():
    dto = SubscriberSchema(email="test@example.com")
    subscriber = await SubscriberService.create(dto)
    assert subscriber.email == "test@example.com"
