from src.apps.public.event.models import Event, EventDate
from src.utilities.base_service import BaseObjectService
from src.error.base import ErrorHandler
from src.enums.base import ContentStatus
from slugify import slugify
from src.apps.file import File
from src.apps.auth.user import User
from src.apps.public.event.schemas import EventSchema, EventDateSchema




class EventService:
    boa = BaseObjectService(Event)
    error = ErrorHandler(Event)
    file = BaseObjectService(File)
    date = BaseObjectService(EventDate)

    @classmethod
    async def all(cls, added_by: str | None = None, category: str | None = None, page: int = 1, count: int = 10):
        query = cls.boa.model.filter(
            is_deleted=False,
            status=ContentStatus.PUBLISH
        ).select_related("added_by").prefetch_related("images")  # M2M

        if added_by:
            query = query.filter(
                added_by__first_name__icontains=added_by
            ) | query.filter(
                added_by__last_name__icontains=added_by
            )

        if category:
            query = query.filter(category__title__icontains=category)

        total = await query.count()
        offset = (page - 1) * count
        query = query.offset(offset).limit(count)
        events = await query.all()

        results = []
        for event in events:
            results.append({
                "id": str(event.id),
                "title": event.title,
                "slug": event.slug,
                "description": event.description,
                "status": event.status,
                "venue": event.venue,
                "added_by": f"{event.added_by.first_name} {event.added_by.last_name}" if event.added_by else None,
                "images": [image.url for image in event.images],
                "map_link": event.map_link,
                "created_at": event.created_at,
                "updated_at": event.updated_at,
            })

        return {
            "page": page,
            "page_size": count,
            "total": total,
            "data": results,
        }

    @classmethod
    async def create(cls, user: User, dto: EventSchema):
        event = await cls.boa.model.create(
            **dto.dict(exclude={"image_ids"}),
            added_by=user
        )

        if dto.image_ids:
            for image_id in dto.image_ids:
                image = await cls.file.model.get_or_none(id=image_id)
                if image:
                    await event.images.add(image)

        return event

    
    @classmethod
    async def delete(cls, id: str):
        return await cls.boa.trash(id=id)
    
    @classmethod
    async def update(cls, id: str, dto: EventSchema):
        event = await cls.boa.get_object_or_404(id=id)
        if not event:
            raise cls.error.get(404, "Event not found")
        data = dto.dict(exclude_unset=True, exclude={"added_by"})
        for field, value in data.items():
            setattr(event, field, value)
        if "title" in data and data["title"]:
            event.slug = slugify(data["title"])
        if dto.image_ids:
            for image_id in dto.image_ids:
                image = await cls.file.model.get_or_none(id=image_id)
                if image:
                    await event.images.add(image)

        return await event.save()
    
    @classmethod
    async def get(cls, id: str | None = None, slug: str | None = None):

        if not id and not slug:
            raise cls.error.get(400, "Provide either 'id' or 'slug' to fetch the event.")

        query = cls.boa.model.filter(is_deleted=False, status=ContentStatus.PUBLISH)
        
        if id:
            query = query.filter(id=id)
        elif slug:
            query = query.filter(slug=slug)
        
        event = await query.prefetch_related("images").select_related("added_by").first()
        
        if not event:
            raise cls.error.get(404, "Event not found")
        
        return {
            "id": str(event.id),
            "title": event.title,
            "slug": event.slug,
            "description": event.description,
            "status": event.status,
            "venue": event.venue,
            "added_by": f"{event.added_by.first_name} {event.added_by.last_name}" if event.added_by else None,
            "images": [image.url for image in event.images],
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }


class EventDateService:
    boa = BaseObjectService(EventDate)
    error = ErrorHandler(EventDate)

    @classmethod
    async def create(cls, dto: EventDateSchema):
        return await cls.boa.model.create(**dto.dict())
    

    @classmethod 
    async def get(cls, event_id):
        return await cls.boa.filter_object(event_id=event_id)
    

    @classmethod
    async def update(cls, event_date_id: str, dto: EventDateSchema):
        """Update an existing event date record."""
        instance = await cls.error.get_or_404(event_date_id)
        update_data = dto.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(instance, key, value)

        return await instance.save()
       

    @classmethod
    async def delete(cls, event_date_id: str):
        return await cls.boa.trash(id=event_date_id)