from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "eventdate" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "date" DATE NOT NULL,
    "start_time" TIMETZ,
    "end_time" TIMETZ,
    "event_id" UUID NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "eventdate";"""
