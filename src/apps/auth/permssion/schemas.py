from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import Action, Resource

class PermissionSchema(BaseModel):
    resource: Optional[Resource] 
    action: Optional[Action]


class PermissionGroupSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permission_ids: Optional[List[str]] = []
