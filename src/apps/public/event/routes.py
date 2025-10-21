from uuid import UUID
from fastapi import Depends, Query, Path, Body
from src.utilities.route_builder import build_router
from src.apps.public.event.services import EventService, EventDateService
from src.apps.public.event.schemas import EventSchema, EventDateSchema
from src.apps.auth.user import User
from src.utilities.crypto import  JWTService

event_router = build_router(path="events", tags=["Events"])
jwt = JWTService()

@event_router.get("", status_code=200)
async def all_events(
    added_by: str | None = Query(None, description="Filter by added_by's name"),
    category: str | None = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    count: int = Query(10, ge=1, le=100, description="Items per page"),
):
    return await EventService.all(added_by=added_by, category=category, page=page, count=count)


@event_router.get("/{slug_or_id}", status_code=200)
async def get_event(slug_or_id: str):
    """Get a single event by ID (UUID) or slug."""

    try:
        UUID(slug_or_id)
        return await EventService.get(id=slug_or_id)
    except ValueError:
        return await EventService.get(slug=slug_or_id)


@event_router.post("", status_code=201)
async def create_event(
    dto: EventSchema = Body(...),
    user: User = Depends(jwt.get_current_user),
):
    return await EventService.create(user, dto)


@event_router.patch("/{id}", status_code=200)
async def update_event(
    id: str = Path(..., description="Event ID"),
    dto: EventSchema = Body(...),
    user: User = Depends(jwt.get_current_user),
):
    """Update an event by ID."""
    return await EventService.update(id, dto)


@event_router.delete("/{id}", status_code=204)
async def delete_event(id: str):
    return await EventService.delete(id=id)



@event_router.post("/dates", status_code=201)
async def create_event_date(dto: EventDateSchema):
    return await EventDateService.create(dto=dto)
 
@event_router.get("/dates/{event_id}", status_code=200)
async def get_event_date(event_id: str):
    return await EventDateService.get(event_id=event_id)



@event_router.patch("/dates/{id}", status_code=200)
async def update_event_date(id: str, dto: EventDateSchema):
    return await EventDateService.update(id=id, dto=dto)


@event_router.delete("/dates/{id}", status_code=200)
async def delete_event_date(id: str):
    return await EventDateService.delete(id=id)