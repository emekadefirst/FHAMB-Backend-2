from fastapi import BackgroundTasks, Query, Depends
from src.utilities.route_builder import build_router
from src.apps.public.mail.services import EmailRouteService
from src.apps.public.mail.schemas import EmailSchema
from src.core.cache import cache  # ✅ Added import

from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService


mail_router = build_router(path="mails", tags=["Mail"])


@mail_router.post(
    "/", 
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_mail(dto: EmailSchema, task: BackgroundTasks):
    return await EmailRouteService.create_mail(dto=dto, task=task)


# @cache(ttl=180)  # ✅ Cached for 3 minutes
@mail_router.get(
    "/",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
)
async def list_mail(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    return await EmailRouteService.all_mail(limit=limit, offset=offset)


# @cache(ttl=120)  # ✅ Cached for 2 minutes
@mail_router.get(
    "/search",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
)
async def search_mail(
    query: str = Query(..., min_length=1, description="Search text for subject, body, sender, or recipients"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await EmailRouteService.search_mail(query=query, limit=limit, offset=offset)
