from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import Action, Resource

class PermissionSchema(BaseModel):
    id: Optional[str] = None
    resource: Optional[Resource] 
    action: Optional[Action]

    class Config:
        from_attributes = True


class PermissionGroupSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permission_ids: Optional[List[str]] = []



class PaginatedPermissionSchema(BaseModel):
    page: int
    page_size: int
    total: int
    results: List[PermissionSchema]