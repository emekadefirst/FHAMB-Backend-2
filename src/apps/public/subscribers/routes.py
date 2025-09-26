from fastapi import BackgroundTasks
from src.utilities.route_builder import build_router
from src.apps.public.subscribers.services import SubscriberService
from src.apps.public.subscribers.schemas import SubscriberSchema

subscriber_router = build_router(path="subscriber", tags=["Subscriber"])

@subscriber_router.post("/")
async def create_subscriber(data: SubscriberSchema):
    return await SubscriberService.create(data)

@subscriber_router.patch("/{id}")
async def update_subscriber(id: str, data: SubscriberSchema):
    return await SubscriberService.update(id, data)

@subscriber_router.get("/{id}")
async def get_subscriber(id: str):
    return await SubscriberService.get(id=id)

@subscriber_router.get("/")
async def list_subscriber():
    return await SubscriberService.all()
