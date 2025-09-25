from fastapi import Request, Depends
from src.utilities.route_builder import build_router
from src.apps.auth.permssion.services import (
    PermissionModelService,
    PermissionGroupModelService,
)
from src.apps.auth.permssion.schemas import PermissionSchema, PermissionGroupSchema
from src.apps.auth.user.services import UserService
from src.apps.auth.user import User


permission_route = build_router(path="permissions", tags=["Permission"])
permission_group_route = build_router(path="permission-groups", tags=["PermissionGroup"])


# ---------------- PERMISSION ROUTES ---------------- #

@permission_route.get("/", status_code=200)
async def list_permissions(current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.fetch_all_permissions()


@permission_route.post("/", status_code=201)
async def create_permission(dto: PermissionSchema, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.create_permission(dto)


@permission_route.get("/{permission_id}", status_code=200)
async def get_permission(permission_id: str, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.fetch_permission_by_id(permission_id)


@permission_route.patch("/{permission_id}", status_code=200)
async def update_permission(permission_id: str, dto: PermissionSchema, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.update_permission(permission_id, dto)


@permission_route.delete("/{permission_id}", status_code=200)
async def delete_permission(permission_id: str, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionModelService.delete_permission(permission_id)


# ---------------- PERMISSION GROUP ROUTES ---------------- #

@permission_group_route.get("/", status_code=200)
async def list_permission_groups(current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionGroupModelService.fetch_all_permission_groups()


@permission_group_route.post("/", status_code=201)
async def create_permission_group(dto: PermissionGroupSchema, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionGroupModelService.create_permission_group(dto)


@permission_group_route.get("/{group_id}", status_code=200)
async def get_permission_group(group_id: str, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionGroupModelService.fetch_permission_group_by_id(group_id)


@permission_group_route.patch("/{group_id}", status_code=200)
async def update_permission_group(group_id: str, dto: PermissionGroupSchema, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionGroupModelService.update_permission_group(group_id, dto)


@permission_group_route.delete("/{group_id}", status_code=200)
async def delete_permission_group(group_id: str, current_user: User = Depends(UserService.jwt.get_current_user)):
    return await PermissionGroupModelService.delete_permission_group(group_id)
