from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "branch" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "address" TEXT NOT NULL,
    "hq" BOOL NOT NULL DEFAULT False,
    "phone_numbers" TEXT[],
    "emails" TEXT[]
);
CREATE TABLE IF NOT EXISTS "contact_us" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "sender_email" VARCHAR(255) NOT NULL,
    "sender_name" VARCHAR(255) NOT NULL,
    "body" TEXT NOT NULL,
    "inquiry_type" VARCHAR(255),
    "phone_number" VARCHAR(20),
    "contact_address" TEXT
);
CREATE TABLE IF NOT EXISTS "mail_email" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "sender" VARCHAR(255) NOT NULL,
    "subject" VARCHAR(255) NOT NULL,
    "recipients" JSONB NOT NULL,
    "body" TEXT NOT NULL,
    "status" VARCHAR(7) NOT NULL DEFAULT 'pending',
    "category" VARCHAR(13) NOT NULL DEFAULT 'notification'
);
COMMENT ON COLUMN "mail_email"."status" IS 'PENDING: pending\nSENT: sent\nFAILED: failed';
COMMENT ON COLUMN "mail_email"."category" IS 'PROMOTIONAL: promotional\nTRANSACTIONAL: transactional\nNOTIFICATION: notification\nNEWSLETTER: newsletter';
CREATE TABLE IF NOT EXISTS "files" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(150) NOT NULL,
    "slug" VARCHAR(250) NOT NULL UNIQUE,
    "type" VARCHAR(8) NOT NULL,
    "extension" VARCHAR(10),
    "mime_type" VARCHAR(100),
    "url" VARCHAR(500) NOT NULL,
    "size" BIGINT NOT NULL,
    "width" INT,
    "height" INT,
    "duration" DOUBLE PRECISION,
    "is_public" BOOL NOT NULL DEFAULT True,
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE INDEX IF NOT EXISTS "idx_files_slug_1c60f3" ON "files" ("slug");
COMMENT ON COLUMN "files"."type" IS 'IMAGE: image\nVIDEO: video\nDOCUMENT: document\nAUDIO: audio';
CREATE TABLE IF NOT EXISTS "permissions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "action" VARCHAR(6) NOT NULL,
    "resource" VARCHAR(10) NOT NULL
);
COMMENT ON COLUMN "permissions"."action" IS 'READ: read\nCREATE: create\nUPDATE: update\nDELETE: delete';
COMMENT ON COLUMN "permissions"."resource" IS 'FILE: file\nUSER: user\nMAIL: mail\nCONTACT: contact\nSUBCRIBER: subscriber';
CREATE TABLE IF NOT EXISTS "permission_groups" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "social" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "url" VARCHAR(550) NOT NULL
);
CREATE TABLE IF NOT EXISTS "subscribers" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "email" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "team" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "position" VARCHAR(255) NOT NULL,
    "about" TEXT,
    "rank" INT,
    "image_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "ip_address" VARCHAR(45),
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "first_name" VARCHAR(30) NOT NULL,
    "last_name" VARCHAR(30) NOT NULL,
    "other_name" VARCHAR(30),
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "phone_number" VARCHAR(15) UNIQUE,
    "contact_address" VARCHAR(255),
    "password" TEXT,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_verified" BOOL NOT NULL DEFAULT False,
    "is_superuser" BOOL NOT NULL DEFAULT False,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "profile_picture" VARCHAR(500),
    "last_login" TIMESTAMPTZ,
    "has_agreed_to_terms" BOOL NOT NULL DEFAULT False
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "mail_email_files" (
    "mail_email_id" UUID NOT NULL REFERENCES "mail_email" ("id") ON DELETE CASCADE,
    "file_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_mail_email__mail_em_d0bcda" ON "mail_email_files" ("mail_email_id", "file_id");
CREATE TABLE IF NOT EXISTS "permission_groups_permissions" (
    "permission_groups_id" UUID NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE,
    "permission_id" UUID NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_permission__permiss_4949c5" ON "permission_groups_permissions" ("permission_groups_id", "permission_id");
CREATE TABLE IF NOT EXISTS "team_social" (
    "team_id" UUID NOT NULL REFERENCES "team" ("id") ON DELETE CASCADE,
    "social_id" UUID NOT NULL REFERENCES "social" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_team_social_team_id_186469" ON "team_social" ("team_id", "social_id");
CREATE TABLE IF NOT EXISTS "users_permission_groups" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "permissiongroup_id" UUID NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_users_permi_users_i_9954a4" ON "users_permission_groups" ("users_id", "permissiongroup_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
