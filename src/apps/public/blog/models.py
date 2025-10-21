from src.utilities.base_model import BaseModel
from tortoise import fields
from src.enums.base import ContentStatus
from slugify import slugify


class Category(BaseModel):
    title = fields.CharField(150, unique=True)
    slug = fields.CharField(150, unique=True, null=True)
    added_by = fields.ForeignKeyField("models.User", related_name="category_user")

    def __str__(self):
        return self.title

    async def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        return await super().save(*args, **kwargs)

    class Meta:
        table = "blogs"
        ordering = ['-created_at', '-updated_at']
        indexes = [
            ('title',),
            ('slug',),
            ('created_at', 'updated_at'),
            ('added_by',)
        ]

class Blog(BaseModel):
    title = fields.CharField(255, unique=True)
    slug = fields.CharField(255, unique=True, null=True)
    content = fields.TextField()
    status = fields.CharEnumField(ContentStatus, default=ContentStatus.DRAFT)
    category = fields.ForeignKeyField("models.Category", related_name="blogs")
    author = fields.ForeignKeyField("models.User", related_name="blogs")
    images = fields.ManyToManyField("models.File", related_name="blogs_images")
    views_count = fields.IntField(default=0)
    tags = fields.JSONField(null=True)

    def __str__(self):
        return self.title

    async def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        return await super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        indexes = [
            ('title',),
            ('slug',),
            ('category', 'author'),
            ('tags',)
        ]
