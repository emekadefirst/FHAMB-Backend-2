from fastapi import Request, Depends, Response, Query, Cookie
from src.apps.auth.user import User
from typing import List, Optional
from src.utilities.route_builder import build_router
from src.apps.auth.user.schemas import UserCreateDto, UserLogin, UserObjectDto, UpdateUserSchema
from src.apps.auth.user.services import UserService
from src.utilities.crypto import JWTService

user_route = build_router(path="users", tags=["User"])
jwt = JWTService()

@user_route.get("/", status_code=200)
async def get_all(
    is_staff: Optional[bool] = Query(None),
    is_admin: Optional[bool] = Query(None),
    is_verified: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await UserService.all(is_staff, is_admin, is_verified, limit, offset)

@user_route.post("/", status_code=201)
async def create_user(dto: UserCreateDto, request: Request, response: Response):
    return await UserService.create_user(dto=dto, request=request, response=response)


@user_route.post("/login", status_code=200)
async def login(dto: UserLogin, request: Request, response: Response):
    return await UserService.login_user(dto=dto, request=request, response=response)

@user_route.get("/whoami", status_code=200, response_model=UserObjectDto)
async def user_profile(current_user: User = Depends(UserService.jwt.get_current_user)):
    return current_user


@user_route.patch("/{id}", status_code=200)
async def update_profile(id: str, dto: UpdateUserSchema):
    return await UserService.update_user(id=id, dto=dto)


@user_route.get("/refresh", status_code=200)
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        return {"error": "Missing refresh token"}
    return await UserService.refresh_access(refresh_token, response)
