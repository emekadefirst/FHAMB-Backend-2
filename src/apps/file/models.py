from tortoise import fields
from tortoise.models import Model
from src.utilities.base_model import BaseModel
from src.enums.base import FileType
from slugify import slugify  

class File(BaseModel):
    name = fields.CharField(max_length=150)
    slug = fields.CharField(max_length=250, unique=True, index=True)
    type = fields.CharEnumField(FileType)
    extension = fields.CharField(max_length=10, null=True)
    mime_type = fields.CharField(max_length=100, null=True)
    url = fields.CharField(max_length=500) 
    size = fields.BigIntField() 
    width = fields.IntField(null=True) 
    height = fields.IntField(null=True)
    duration = fields.FloatField(null=True) 
    is_public = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "files"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}.{self.extension} ({self.type})"

    async def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while await File.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        await super().save(*args, **kwargs)
