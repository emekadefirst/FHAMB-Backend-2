from src.utilities.base_model import BaseModel
from tortoise import fields
from slugify import slugify
from src.enums.base import ContentStatus

class FAQ(BaseModel):
    question = fields.CharField(500, unique=True)
    slug = fields.CharField(500, unique=True, null=True)
    answer = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="faq_author")
    status = fields.CharEnumField(ContentStatus, default=ContentStatus.PUBLISH) 
    category = fields.ForeignKeyField("models.Category", related_name="faq_category", on_delete=fields.SET_NULL, null=True)


    def __str__(self):
        return self.question

    async def save(self, *args, **kwargs):
        if not self.slug and self.question:
            self.slug = slugify(self.question)
        return await super().save(*args, **kwargs)

    class Meta:
        table = "faqs"
        ordering = ['-created_at', '-updated_at']
        indexes = [
            ('question',),
            ('slug',),
            ('category',),
        ]
