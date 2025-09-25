from fastapi import Request, Depends, Response
from src.apps.auth.user import User
from src.utilities.route_builder import build_router
from src.apps.auth.user.schemas import UserCreateDto, UserLogin, UserObjectDto
from src.apps.auth.user.services import UserService
from src.utilities.crypto import JWTService

user_route = build_router(path="users", tags=["User"])
jwt = JWTService()


@user_route.post("/", status_code=201)
async def create_user(dto: UserCreateDto, request: Request, response: Response):
    return await UserService.create_user(dto=dto, request=request, response=response)


@user_route.post("/login", status_code=200)
async def login(dto: UserLogin, request: Request, response: Response):
    return await UserService.login_user(dto=dto, request=request, response=response)

@user_route.get("/whoami", status_code=200, response_model=UserObjectDto)
async def user_profile(current_user: User = Depends(UserService.jwt.get_current_user)):
    return current_user

