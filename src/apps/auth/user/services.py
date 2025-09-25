from fastapi import Request, BackgroundTasks, Response
from src.utilities.base_service import BaseObjectService
from src.apps.auth.user.models import User
from src.error.base import ErrorHandler
from src.apps.auth.user.schemas import UserCreateDto, UserLogin
from src.libs.smtp.mailer import EmailService
from src.utilities.crypto import JWTService
from src.utilities.meta import get_ipaddr
from tortoise import timezone
from src.utilities.hash import verify_password


class UserService:
    boa = BaseObjectService(User)
    model = User
    error = ErrorHandler(User)
    email = EmailService()
    jwt = JWTService()

    task = BackgroundTasks

    @classmethod
    async def create_user(cls, dto: UserCreateDto, request: Request, response: Response):
        ip_addr = get_ipaddr(request=request)
        existing_user = await cls.boa.get_object_or_404(email=dto.email, phone_number=dto.phone_number)
        if existing_user:
            if existing_user.email == dto.email:
                raise cls.error.get(409, "Email already exist. Try another one")
            if existing_user.phone_number == dto.phone_number:
                raise cls.error.get(409, "Phone number already exist. Try another one")
        user = await cls.model.create(**dict(dto))
        user.ip_address = ip_addr
        await user.save()
        token = cls.jwt.generate_token(str(user.id))
        response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=900,
            path="/"

        )
        response.set_cookie(
            key="refresh_token",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"

        )


    @classmethod
    async def login_user(cls, dto: UserLogin, request: Request, response: Response):
        user = await cls.boa.get_object_or_404(email=dto.email)
        if not user:
            raise cls.error.get(400)
        password = verify_password(hashed_password=user.password, plain_password=dto.password)
        if password is not None:
            user.last_login = timezone.now()
        ip_address = get_ipaddr(request=request)
        if ip_address != user.ip_address and dto.device_id != user.device_id:
            user.ip_address = ip_address
            user.device_id = dto.device_id
            user.is_active = False
            await user.save()
        user.latitude = dto.latitude
        user.logitude = dto.longitude
        await user.save()
        token = cls.jwt.generate_token(str(user.id))

        response.set_cookie(
                key="access_token",
                value=token["access_token"],
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=900,
                path="/"
            )
        response.set_cookie(
            key="refresh_token",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"
        )  

    @classmethod
    async def all(cls):
        users = await cls.model.all().prefetch_related("permission_groups")
        results = []
        for user in users:
            results.append({
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "other_name": user.other_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "contact_address": user.contact_address,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "profile_picture": user.profile_picture,
                "is_deleted": user.is_deleted,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "has_agreed_to_terms": user.has_agreed_to_terms,
                "latitude": user.latitude,
                "longitude": user.longitude,
                "device_id": user.device_id,
                "ip_address": user.ip_address,
                "permission_groups": user.permission_groups if user.permission_groups else None if user.permission_groups else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            })
        return results
    
    @classmethod
    async def get(cls, user_id: str):
        user = await cls.model.get_or_none(id=user_id).prefetch_related("role")
        if not user:
            return None
        
        return {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "other_name": user.other_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "contact_address": user.contact_address,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "profile_picture": user.profile_picture,
            "is_deleted": user.is_deleted,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "has_agreed_to_terms": user.has_agreed_to_terms,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "device_id": user.device_id,
            "ip_address": user.ip_address,
            "permission_groups": user.permission_groups if user.permission_groups else None if user.permission_groups else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
    
    @classmethod
    async def generate_access(cls, refresh_token: str):
        token = JWTService.refresh_token(refresh_token)
        cls.response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=900,
            path="/"

        )
        cls.response.set_cookie(
            key="refresh_token",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"

        )
