from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "events" ADD "map_link" VARCHAR(600);
        ALTER TABLE "permissions" ALTER COLUMN "resource" TYPE VARCHAR(6) USING "resource"::VARCHAR(6);
        COMMENT ON COLUMN "permissions"."resource" IS 'FILE: file
AUTH: auth
MAIL: mail
PUBLIC: public';
        ALTER TABLE "team" ALTER COLUMN "image_id" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "team" ALTER COLUMN "image_id" SET NOT NULL;
        ALTER TABLE "events" DROP COLUMN "map_link";
        COMMENT ON COLUMN "permissions"."resource" IS 'FILE: file
USER: user
MAIL: mail
CONTACT: contact
SUBCRIBER: subscriber';
        ALTER TABLE "permissions" ALTER COLUMN "resource" TYPE VARCHAR(10) USING "resource"::VARCHAR(10);"""
