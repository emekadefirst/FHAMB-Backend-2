from slugify import slugify
from tortoise.expressions import Q, Case, When
from tortoise.fields import IntField
from src.utilities.base_service import BaseObjectService
from src.apps.public.gallery import Gallery
from src.apps.public.gallery.schema import GallerySchema
from src.error.base import ErrorHandler
from src.apps.file.models import File 


class GalleryService:
    boa = BaseObjectService(Gallery)
    error = ErrorHandler(Gallery)

    @classmethod
    async def create(cls, dto: GallerySchema):
        data = dto.dict(exclude_unset=True)
        if not data.get("slug") and data.get("title"):
            data["slug"] = slugify(data["title"])

        gallery = await cls.boa.model.create(**data)

       
        image_ids = data.get("image_ids", [])
        if image_ids:
            for image_id in image_ids:
                image = await File.get_or_none(id=image_id)
                if image:
                    await gallery.images.add(image)

        return gallery

    @classmethod
    async def all(cls, author: str | None = None, category: str | None = None):
        query = (
            cls.boa.model.filter(is_deleted=False)
            .select_related("author", "category")
            .prefetch_related("images")
        )

        if author:
            query = query.filter(
                Q(author__first_name__icontains=author)
                | Q(author__last_name__icontains=author)
            )
        if category:
            query = query.filter(category__name__icontains=category)

        return await query.all()

    @classmethod
    async def get(cls, id: str):
        obj = await cls.boa.get_object(id=id)
        if not obj:
            return await cls.error.not_found("Gallery not found")
        return obj

    @classmethod
    async def update(cls, id: str, dto: GallerySchema):
        obj = await cls.boa.get_object(id=id)
        if not obj:
            return await cls.error.not_found("Gallery not found")

        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        if not obj.slug and obj.title:
            obj.slug = slugify(obj.title)

        # ✅ Handle images
        if "image_ids" in update_data:
            await obj.images.clear()
            for image_id in update_data["image_ids"]:
                image = await File.get_or_none(id=image_id)
                if image:
                    await obj.images.add(image)

        await obj.save()
        return obj

    @classmethod
    async def delete(cls, id: str):
        obj = await cls.boa.get_object(id=id)
        if not obj:
            return await cls.error.not_found("Gallery not found")
        await obj.delete()
        return {"message": "Gallery deleted successfully"}

    @classmethod
    async def search(cls, query: str):
        """
        Search galleries by title, description, category name, or author name.
        Prioritize exact matches first.
        """
        if not query or not query.strip():
            return await cls.error.get(404, "Search query cannot be empty")

        results = (
            cls.boa.model.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            )
            .annotate(
                exact_match=Case(
                    When(title__iexact=query, then=1),
                    default=0,
                    output_field=IntField()
                )
            )
            .filter(is_deleted=False)
            .order_by("-exact_match", "-created_at")
            .select_related("author", "category")
            .prefetch_related("images")
        )

        return await results.all()
