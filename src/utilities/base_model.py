from tortoise import Model, fields, timezone
import uuid

class BaseModel(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, editable=False)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)
    is_deleted = fields.BooleanField(default=False)

    async def save(self, using_db = None, update_fields = None, force_create = False, force_update = False):
        if self.id:
            self.updated_at = timezone.now()
        return await super().save(using_db, update_fields, force_create, force_update)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]






