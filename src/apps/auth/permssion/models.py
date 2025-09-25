from src.utilities.base_model import BaseModel
from tortoise import fields
from src.enums.base import Action, Resource


class Permission(BaseModel):
    action = fields.CharEnumField(Action)
    resource = fields.CharEnumField(Resource)

    class Meta:
        ordering = ['created_at', 'updated_at']
        table = "permissions"

    def __str__(self):
        return f"Permission: {self.action} actions on {self.module}."
    

class PermissionGroup(BaseModel):
    name = fields.CharField(100, unique=True)
    permissions = fields.ManyToManyField("models.Permission", related_name="groups") 

    class Meta:
        ordering = ['created_at', 'updated_at']
        table = "permission_groups"

    def __str__(self):
        return self.name