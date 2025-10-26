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
    "sender_email" VARCHAR(55) NOT NULL,
    "sender_name" VARCHAR(55) NOT NULL,
    "body" VARCHAR(200) NOT NULL,
    "inquiry_type" VARCHAR(150),
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
    "public" BOOL NOT NULL DEFAULT False,
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
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
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
    "last_login" TIMESTAMPTZ,
    "has_agreed_to_terms" BOOL NOT NULL DEFAULT False,
    "device_id" VARCHAR(100) UNIQUE,
    "ip_address" VARCHAR(45),
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "profile_picture_id" UUID REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "blogs" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(150) NOT NULL UNIQUE,
    "slug" VARCHAR(150) UNIQUE,
    "added_by_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_blogs_title_787d73" ON "blogs" ("title");
CREATE INDEX IF NOT EXISTS "idx_blogs_slug_08f29d" ON "blogs" ("slug");
CREATE INDEX IF NOT EXISTS "idx_blogs_created_6cefa5" ON "blogs" ("created_at", "updated_at");
CREATE INDEX IF NOT EXISTS "idx_blogs_added_b_383cc2" ON "blogs" ("added_by_id");
CREATE TABLE IF NOT EXISTS "blog" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(255) NOT NULL UNIQUE,
    "slug" VARCHAR(255) UNIQUE,
    "content" TEXT NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'draft',
    "views_count" INT NOT NULL DEFAULT 0,
    "tags" JSONB,
    "author_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "category_id" UUID NOT NULL REFERENCES "blogs" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_blog_title_346fdb" ON "blog" ("title");
CREATE INDEX IF NOT EXISTS "idx_blog_slug_5f3eb1" ON "blog" ("slug");
CREATE INDEX IF NOT EXISTS "idx_blog_categor_f8baad" ON "blog" ("category_id", "author_id");
CREATE INDEX IF NOT EXISTS "idx_blog_tags_9cffb4" ON "blog" ("tags");
COMMENT ON COLUMN "blog"."status" IS 'PUBLISH: published\nDRAFT: draft';
CREATE TABLE IF NOT EXISTS "events" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(255) NOT NULL UNIQUE,
    "slug" VARCHAR(255) UNIQUE,
    "description" TEXT,
    "status" VARCHAR(9) NOT NULL DEFAULT 'draft',
    "venue" VARCHAR(255),
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "added_by_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_events_title_44f4d6" ON "events" ("title");
CREATE INDEX IF NOT EXISTS "idx_events_slug_bbf41e" ON "events" ("slug");
COMMENT ON COLUMN "events"."status" IS 'PUBLISH: published\nDRAFT: draft';
CREATE TABLE IF NOT EXISTS "faqs" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "question" VARCHAR(500) NOT NULL UNIQUE,
    "slug" VARCHAR(500) UNIQUE,
    "answer" TEXT NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'published',
    "author_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "category_id" UUID REFERENCES "blogs" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_faqs_questio_b433b3" ON "faqs" ("question");
CREATE INDEX IF NOT EXISTS "idx_faqs_slug_ea8a16" ON "faqs" ("slug");
CREATE INDEX IF NOT EXISTS "idx_faqs_categor_49f7ee" ON "faqs" ("category_id");
COMMENT ON COLUMN "faqs"."status" IS 'PUBLISH: published\nDRAFT: draft';
CREATE TABLE IF NOT EXISTS "gallery" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(255) NOT NULL UNIQUE,
    "slug" VARCHAR(255) UNIQUE,
    "description" TEXT,
    "status" VARCHAR(9) NOT NULL DEFAULT 'draft',
    "views_count" INT NOT NULL DEFAULT 0,
    "author_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "category_id" UUID NOT NULL REFERENCES "blogs" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_gallery_title_e20ba5" ON "gallery" ("title");
CREATE INDEX IF NOT EXISTS "idx_gallery_slug_a8a526" ON "gallery" ("slug");
CREATE INDEX IF NOT EXISTS "idx_gallery_categor_a11b36" ON "gallery" ("category_id", "author_id");
COMMENT ON COLUMN "gallery"."status" IS 'PUBLISH: published\nDRAFT: draft';
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
    "users_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "permissiongroup_id" UUID NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_users_permi_users_i_9954a4" ON "users_permission_groups" ("users_id", "permissiongroup_id");
CREATE TABLE IF NOT EXISTS "blog_files" (
    "blog_id" UUID NOT NULL REFERENCES "blog" ("id") ON DELETE CASCADE,
    "file_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_blog_files_blog_id_85b10f" ON "blog_files" ("blog_id", "file_id");
CREATE TABLE IF NOT EXISTS "events_files" (
    "events_id" UUID NOT NULL REFERENCES "events" ("id") ON DELETE SET NULL,
    "file_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_events_file_events__67c994" ON "events_files" ("events_id", "file_id");
CREATE TABLE IF NOT EXISTS "gallery_files" (
    "gallery_id" UUID NOT NULL REFERENCES "gallery" ("id") ON DELETE CASCADE,
    "file_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_gallery_fil_gallery_814c51" ON "gallery_files" ("gallery_id", "file_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
