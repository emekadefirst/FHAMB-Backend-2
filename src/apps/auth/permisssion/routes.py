from fastapi import Request, Depends
from src.utilities.route_builder import build_router
from src.apps.auth.permisssion.services import (
    PermissionModelService,
    PermissionGroupModelService,
)
from src.apps.auth.permisssion.schemas import (
    PermissionSchema,
    PermissionGroupSchema,
    PermissionListResponse,
    PermissionGroupListResponse,
    PermissionGroupObject
)
from src.apps.auth.user.services import UserService
from src.apps.auth.permisssion.models import Permission, PermissionGroup
from src.apps.auth.user import User
from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService
from src.core.cache import cache

permission_route = build_router(path="permissions", tags=["Permission"])
permission_group_route = build_router(path="permission-groups", tags=["PermissionGroup"])


# ---------------- PERMISSION ROUTES ---------------- #

@permission_route.get(
    "/",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.AUTH))]
)
@cache(ttl=300)
async def list_permissions(request: Request):
    return  await PermissionModelService.fetch_all_permissions()


@permission_route.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.AUTH))]
)
async def create_permission(dto: PermissionSchema):
    return await PermissionModelService.create_permission(dto)


@permission_route.get(
    "/{permission_id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.AUTH))]
)
@cache(ttl=600)
async def get_permission(permission_id: str, request: Request, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.fetch_permission_by_id(permission_id)


@permission_route.patch(
    "/{permission_id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.AUTH))]
)
async def update_permission(permission_id: str, dto: PermissionSchema, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.update_permission(permission_id, dto)


@permission_route.delete(
    "/{permission_id}",
    status_code=204,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.AUTH))]
)
async def delete_permission(permission_id: str, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.delete_permission(permission_id)


# ---------------- PERMISSION GROUP ROUTES ---------------- #

@permission_group_route.get(
    "/",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.AUTH))]
)
# @cache(ttl=300)
async def list_permission_groups(request: Request):
    return await PermissionGroupModelService.fetch_all_permission_groups()
   


@permission_group_route.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.AUTH))]
)
async def create_permission_group(dto: PermissionGroupSchema):
    return await PermissionGroupModelService.create_permission_group(dto)


@permission_group_route.get(
    "/{group_id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.AUTH))]
)
# @cache(ttl=600)
async def get_permission_group(group_id: str):
    return await PermissionGroupModelService.fetch_permission_group_by_id(group_id)


@permission_group_route.patch(
    "/{group_id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.AUTH))]
)
async def update_permission_group(group_id: str, dto: PermissionGroupSchema):
    return await PermissionGroupModelService.update_permission_group(group_id, dto)


@permission_group_route.delete(
    "/{group_id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.AUTH))]
)
async def delete_permission_group(group_id: str):
    return await PermissionGroupModelService.delete_permission_group(group_id)
