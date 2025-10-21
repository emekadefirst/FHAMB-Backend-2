from slugify import slugify
from src.utilities.base_service import BaseObjectService
from src.apps.public.faq import FAQ
from src.apps.public.faq.schema import FAQSchema
from src.error.base import ErrorHandler

class FAQService:
    boa = BaseObjectService(FAQ)
    error = ErrorHandler(FAQ)

    @classmethod
    async def create(cls, dto: FAQSchema):
        data = dto.dict()
        if not data.get("slug") and data.get("question"):
            data["slug"] = slugify(data["question"])
        return await cls.boa.model.create(**data)

    @classmethod
    async def all(cls, author: str | None = None, category: str | None = None):
        query = cls.boa.model.filter(is_deleted=False).select_related("author", "category")
        if author:
            query = query.filter(author__first_name__icontains=author) | query.filter(author__last_name__icontains=author)
        if category:
            query = query.filter(category__name__icontains=category)
        return await query

    @classmethod
    async def get(cls, id: str):
        obj = await cls.boa.get_object(id=id)
        if not obj:
            return await cls.error.not_found("FAQ not found")
        return obj

    @classmethod
    async def update(cls, id: str, dto: FAQSchema):
        obj = await cls.boa.get_object(id=id)
        if not obj:
            return await cls.error.not_found("FAQ not found")
        await obj.update_from_dict(dto.dict(exclude_unset=True))
        if not obj.slug and obj.question:
            obj.slug = slugify(obj.question)
        await obj.save()
        return obj

    @classmethod
    async def delete(cls, id: str):
        return await cls.boa.trash(id=id)
