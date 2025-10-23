from fastapi import BackgroundTasks, Depends
from src.utilities.route_builder import build_router
from src.apps.public.subscribers.services import SubscriberService
from src.apps.public.subscribers.schemas import SubscriberSchema
from src.core.cache import cache  # ✅ Added import
from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService

subscriber_router = build_router(path="subscriber", tags=["Subscriber"])

@subscriber_router.post("/", status_code=201)
async def create_subscriber(data: SubscriberSchema):
    return await SubscriberService.create(data)

@subscriber_router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_subscriber(id: str, data: SubscriberSchema):
    return await SubscriberService.update(id, data)

# @cache(ttl=180)  # ✅ Cached for 3 minutes
@subscriber_router.get(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
)
async def get_subscriber(id: str):
    return await SubscriberService.get(id=id)

# @cache(ttl=180)  # ✅ Cached for 3 minutes
@subscriber_router.get(
    "/",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
)
async def list_subscriber():
    return await SubscriberService.all()
