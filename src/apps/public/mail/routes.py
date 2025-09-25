from fastapi import BackgroundTasks, Query
from src.utilities.route_builder import build_router
from src.apps.public.mail.services import EmailRouteService
from src.apps.public.mail.schemas import EmailSchema

mail_router = build_router(path="mail", tags=["Mail"])


@mail_router.post("", status_code=201)
async def create_mail(dto: EmailSchema, task: BackgroundTasks):
    return await EmailRouteService.create_mail(dto=dto, task=task)


@mail_router.get("")
async def list_mail(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    return await EmailRouteService.all_mail(limit=limit, offset=offset)


@mail_router.get("/search")
async def search_mail(
    query: str = Query(..., min_length=1, description="Search text for subject, body, sender, or recipients"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await EmailRouteService.search_mail(query=query, limit=limit, offset=offset)
