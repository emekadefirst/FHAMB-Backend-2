from fastapi import Depends
from src.apps.auth import User
from src.enums.base import Action, Resource
from src.error.base import ErrorHandler
from src.utilities.crypto import JWTService
from src.apps.auth.permisssion import Permission




class AuthPermissionService:
    error = ErrorHandler(Permission)
    jwt = JWTService()

    @classmethod
    async def has_permission(cls, user: User, action: Action, resource: Resource) -> bool:
        if user.is_superuser:
            return True

        groups = await user.permission_groups.all().prefetch_related("permissions")
        for group in groups:
            perms = await group.permissions.all()
            for perm in perms:
                if perm.action == action and perm.resource == resource:
                    return True
        return False

    @staticmethod
    def permission_required(cls, action: Action, resource: Resource):
        async def dependency(user: User = Depends(cls.jwt.get_current_user)):
            if not await AuthPermissionService.has_permission(user, action, resource):
                raise cls.error.get(403)
            return user
        return dependency