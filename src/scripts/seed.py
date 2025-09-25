import asyncio
from tortoise import Tortoise
from src.core.database import TORTOISE_ORM
from src.core.models import User, Permission, PermissionGroup
from src.enums.base import Action, Resource



async def seed_admin_user():
    admin_email = "admin@fhamb.gov.ng"
    admin_password = "Admin25$$"
    first_name = "Admin"
    last_name = "User"
    phone_number = "08025074700"

    existing = await User.filter(email=admin_email).first()
    if existing:
        print(f"⚠️ Admin user already exists: {existing.email}")
        return existing

    user = await User.create(
        email=admin_email,
        first_name=first_name,
        last_name=last_name,
        password=admin_password,
        phone_number=phone_number,  
        is_superuser=True,
        is_staff=True,
        is_host=True,
        is_active=True,
        is_verified=True,
    )
    print(f"✅ Admin user created: {user.email}")
    return user


async def seed_permissions():
    permissions_data = [
        (Action.CREATE, Resource.USER),
        (Action.READ, Resource.USER),
        (Action.UPDATE, Resource.USER),
        (Action.DELETE, Resource.USER),
        (Action.CREATE, Resource.PERMISSION),
        (Action.READ, Resource.PERMISSION),
    ]

    permissions = []
    for action, module in permissions_data:
        perm, _ = await Permission.get_or_create(action=action, module=module)
        permissions.append(perm)

    print(f"✅ Seeded {len(permissions)} permissions")
    return permissions


async def seed_permission_group(permissions):
    group_name = "Admin Group"
    group, _ = await PermissionGroup.get_or_create(name=group_name)
    await group.permissions.add(*permissions)
    print(f"✅ Permission group '{group_name}' seeded with permissions")
    return group


async def main():
    print("🚀 Seeding database...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    permissions = await seed_permissions()
    group = await seed_permission_group(permissions)
    admin_user = await seed_admin_user()
    await admin_user.permission_groups.add(group)

    await Tortoise.close_connections()
    print("🎉 Seeding admin complete!")


def run():
    asyncio.run(main())
