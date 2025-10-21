import asyncio
from tortoise import Tortoise
from src.core.database import TORTOISE_ORM
from src.core.models import User, Permission, PermissionGroup
from src.enums.base import Action, Resource


async def seed_admin_user():
    admin_email = "admin@fhamb.gov.ng"
    admin_password = "Admin25$$"
    first_name = "Default"
    last_name = "Admin"
    phone_number = "8100000000"

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
        is_active=True,
        is_verified=True,
    )
    print(f"✅ Admin user created: {user.email}")
    return user


async def seed_permissions():
    """
    Create CRUD permissions for all defined resources.
    """
    permissions = []

    for resource in Resource:
        for action in Action:
            # Create or get existing permission
            perm, _ = await Permission.get_or_create(
                action=action,
                resource=resource
            )
            permissions.append(perm)

    print(f"✅ Seeded {len(permissions)} permissions (CRUD for {len(Resource)} resources)")
    return permissions


async def seed_permission_group(permissions):
    """
    Create an 'Admin Group' and attach all permissions to it.
    """
    group_name = "Admin Group"
    group, created = await PermissionGroup.get_or_create(name=group_name)

    if created:
        await group.permissions.add(*permissions)
        print(f"✅ Permission group '{group_name}' created with {len(permissions)} permissions")
    else:
        existing_perms = await group.permissions.all().count()
        if existing_perms < len(permissions):
            await group.permissions.add(*permissions)
        print(f"⚙️ Permission group '{group_name}' already exists. Synced {len(permissions)} permissions.")

    return group


async def main():
    print("🚀 Seeding database...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    # Seed permissions and groups
    permissions = await seed_permissions()
    group = await seed_permission_group(permissions)

    # Seed admin user and attach group
    admin_user = await seed_admin_user()
    await admin_user.permission_groups.add(group)

    await Tortoise.close_connections()
    print("🎉 Seeding admin complete!")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
