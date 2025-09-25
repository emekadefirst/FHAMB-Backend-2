from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "device_id" VARCHAR(100) UNIQUE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_users_device__81c5d1" ON "users" ("device_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_users_device__81c5d1";
        ALTER TABLE "users" DROP COLUMN "device_id";"""
