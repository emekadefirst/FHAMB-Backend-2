from src.utilities.base_model import BaseModel
from tortoise import fields
from slugify import slugify
from src.enums.base import ContentStatus

class Gallery(BaseModel):
    title = fields.CharField(255, unique=True)
    slug = fields.CharField(255, unique=True, null=True)
    description = fields.TextField(null=True)
    category = fields.ForeignKeyField("models.Category", related_name="galleries_category")
    author = fields.ForeignKeyField("models.User", related_name="galleries")
    status = fields.CharEnumField(ContentStatus, default=ContentStatus.DRAFT)
    images = fields.ManyToManyField("models.File", related_name="blog_media", on_delete=fields.CASCADE)
    views_count = fields.IntField(default=0)

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
        ]
