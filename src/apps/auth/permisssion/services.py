from src.apps.auth.permisssion import Permission, PermissionGroup
from src.error.base import ErrorHandler
from src.utilities.base_service import BaseObjectService
from src.apps.auth.permisssion.schemas import PermissionSchema, PermissionGroupSchema


class PermissionModelService:
    boa = BaseObjectService(Permission)
    model = Permission
    error = ErrorHandler(Permission)

    @classmethod
    async def fetch_all_permissions(cls):
        return await cls.boa.all()

    @classmethod
    async def create_permission(cls, dto: PermissionSchema):
        return await cls.model.create(**dto.dict(exclude_unset=True))

    @classmethod
    async def update_permission(cls, permission_id: str, dto: PermissionSchema):
        permission = await cls.model.get_or_none(id=permission_id, is_deleted=False)
        if not permission:
            raise cls.error.not_found()
        for attr, value in dto.dict(exclude_unset=True).items():
            setattr(permission, attr, value)
        await permission.save()
        return permission

    @classmethod
    async def fetch_permission_by_id(cls, permission_id: str):
        permission = await cls.model.get_or_none(id=permission_id, is_deleted=False)
        if not permission:
            raise cls.error.not_found()
        return permission

    @classmethod
    async def delete_permission(cls, permission_id: str):
        permission = await cls.model.get_or_none(id=permission_id, is_deleted=False)
        if not permission:
            raise cls.error.not_found()
        permission.is_deleted = True
        await permission.save()
        return permission


class PermissionGroupModelService:
    boa = BaseObjectService(PermissionGroup)
    model = PermissionGroup
    error = ErrorHandler(PermissionGroup)

    @classmethod
    async def fetch_all_permission_groups(cls):
        groups = await cls.model.filter(is_deleted=False).prefetch_related("permissions")
        result = []
        for g in groups:
            result.append({
                "id": str(g.id),
                "name": g.name,
                "permissions": [
                    {
                        "id": p.id,
                        "action": p.action,      # convert Enum -> str
                        "object": p.resource,    # convert Enum -> str
                    }
                    for p in g.permissions
                ],
                "created_at": g.created_at.isoformat() if g.created_at else None,
                "updated_at": g.updated_at.isoformat() if g.updated_at else None,
            })
        return result

    @classmethod
    async def create_permission_group(cls, dto: PermissionGroupSchema):
        group = await cls.model.create(name=dto.name)
        for pid in dto.permission_ids:
            permission = await Permission.get_or_none(id=pid, is_deleted=False)
            if not permission:
                raise ErrorHandler(Permission).not_found()
            await group.permissions.add(permission)
        await group.save()
        return group

    @classmethod
    async def update_permission_group(cls, group_id: str, dto: PermissionGroupSchema):
        group = await cls.model.filter(id=group_id, is_deleted=False).prefetch_related("permissions").first()
        if not group:
            raise cls.error.not_found()
        if dto.name is not None:
            group.name = dto.name
        if dto.permission_ids:
            await group.permissions.clear()
            for pid in dto.permission_ids:
                permission = await Permission.get_or_none(id=pid, is_deleted=False)
                if not permission:
                    raise ErrorHandler(Permission).not_found()
                await group.permissions.add(permission)
        await group.save()
        return group

    @classmethod
    async def fetch_permission_group_by_id(cls, group_id: str):
        group = await cls.model.filter(id=group_id, is_deleted=False).prefetch_related("permissions").first()
        if not group:
            raise cls.error.not_found()
        return {
            "id": str(group.id),
            "name": group.name,
            "permissions": [
                {"action": p.action, "object": p.resource} for p in group.permissions
            ],
            "created_at": group.created_at,
            "updated_at": group.updated_at,
        }

    @classmethod
    async def delete_permission_group(cls, group_id: str):
        return await cls.boa.trash(id=group_id)
