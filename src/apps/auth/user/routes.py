from fastapi import Request, Depends, Response, Query, Cookie
from src.apps.auth.user import User
from typing import Optional
from src.utilities.route_builder import build_router
from src.apps.auth.user.schemas import UserCreateDto, UserLogin, UserObjectDto, UpdateUserSchema
from src.apps.auth.user.services import UserService
from src.utilities.crypto import JWTService
from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService
from src.core.cache import cache   # ✅ added

user_route = build_router(path="users", tags=["User"])
jwt = JWTService()


# -------------------- GET ALL USERS -------------------- #
@user_route.get(
    "/", 
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.AUTH))]
)
# @cache(ttl=300)   # ✅ Cache for 5 minutes (industry standard for listing endpoints)
async def get_all(
    request: Request,
    is_staff: Optional[bool] = Query(None),
    is_admin: Optional[bool] = Query(None),
    is_verified: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await UserService.all(is_staff, is_admin, is_verified, limit, offset)


# -------------------- CREATE USER -------------------- #
@user_route.post(
    "/", 
    status_code=201
)
async def create_user(dto: UserCreateDto, request: Request, response: Response):
    return await UserService.create_user(dto=dto, request=request, response=response)


# -------------------- LOGIN -------------------- #
@user_route.post(
    "/login", 
    status_code=200
)
async def login(dto: UserLogin, request: Request, response: Response):
    return await UserService.login_user(dto=dto, request=request, response=response)


# -------------------- WHOAMI -------------------- #
@user_route.get(
    "/whoami", 
    status_code=200, 
)
# @cache(ttl=120)   # ✅ Cache for 2 minutes (since user details may change)
async def user_profile(request: Request, current_user: User = Depends(UserService.jwt.get_current_user)):
    return current_user


# -------------------- UPDATE USER -------------------- #
@user_route.patch(
    "/{id}", 
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.AUTH))]
)
async def update_profile(id: str, dto: UpdateUserSchema):
    return await UserService.update_user(id=id, dto=dto)


# -------------------- REFRESH TOKEN -------------------- #
@user_route.get("/refresh", status_code=200)
# @cache(ttl=60)   # ✅ Cache for 1 minute (short TTL since tokens refresh frequently)
async def refresh_token(
    request: Request,
    response: Response,
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        return {"error": "Missing refresh token"}
    return await UserService.refresh_access(refresh_token, response)
