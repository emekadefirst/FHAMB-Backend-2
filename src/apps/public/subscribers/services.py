from fastapi import BackgroundTasks
from typing import Optional, List

from src.utilities.base_service import BaseObjectService
from src.apps.public.subscribers import Subscriber
from src.error.base import ErrorHandler
from src.apps.public.subscribers.schemas import SubscriberSchema  # reuse SubscriberSchema for email validation


class SubscriberService:
    boa = BaseObjectService(Subscriber)
    error = ErrorHandler(Subscriber)

    @classmethod
    async def create(cls, data: SubscriberSchema):
        return await cls.boa.model.create(**data.dict())

    @classmethod
    async def update(cls, id: str, data: SubscriberSchema):
        obj = await cls.boa.get_object_or_404(id=id)
        if not obj:
            raise cls.error.get(404)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @classmethod
    async def get(cls, **filters):
        obj = await cls.boa.get_object_or_404(**filters)
        if not obj:
            raise cls.error.get(404)
        return obj

    @classmethod
    async def all(cls):
        return await cls.boa.all()

    @classmethod
    async def delete(cls, id):
        return await cls.boa.trash(id=id)
