from src.utilities.base_model import BaseModel, MetaData
from tortoise import fields
from src.utilities.hash import set_password


class User(BaseModel, MetaData):
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    other_name = fields.CharField(max_length=30, null=True)
    email = fields.CharField(max_length=254, unique=True)
    phone_number = fields.CharField(max_length=15, unique=True, null=True)
    contact_address = fields.CharField(max_length=255, null=True)
    password = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)
    is_verified = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    profile_picture = fields.ForeignKeyField("models.File", related_name="user_profile", null=True)
    last_login = fields.DatetimeField(null=True)
    has_agreed_to_terms = fields.BooleanField(default=False)
    permission_groups = fields.ManyToManyField(
        "models.PermissionGroup"
    )


    class Meta:
        ordering = ["created_at", "updated_at"]
        table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


    async def save(self, *args, **kwargs):
        if self.password: 
            self.password = set_password(self.password)
        await super().save(*args, **kwargs)


