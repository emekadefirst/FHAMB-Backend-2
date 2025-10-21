from src.utilities.base_model import BaseModel
from tortoise import fields
from slugify import slugify
from src.enums.base import ContentStatus

class Event(BaseModel):
    title = fields.CharField(255, unique=True)
    slug = fields.CharField(255, unique=True, null=True)
    description = fields.TextField(null=True)
    added_by = fields.ForeignKeyField("models.User", related_name="event_author")
    status = fields.CharEnumField(ContentStatus, default=ContentStatus.DRAFT)
    venue = fields.CharField(255, null=True)  
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
    images = fields.ManyToManyField("models.File", related_name="event_media", on_delete=fields.SET_NULL, null=True )

    def __str__(self):
        return self.title

    async def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        return await super().save(*args, **kwargs)

    class Meta:
        table = "events"
        ordering = ['-created_at', '-updated_at']
        indexes = [
            ('title',),
            ('slug',),
        ]


class EventDate(BaseModel):
    event = fields.ForeignKeyField("models.Event", related_name="dates")
    date = fields.DateField()
    start_time = fields.TimeField(null=True)
    end_time = fields.TimeField(null=True)

    class Meta:
        ordering = ['date', 'start_time']

