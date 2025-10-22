from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from src.enums.base import Action, Resource

# ---------------- Input Schemas ---------------- #

class PermissionSchema(BaseModel):
    id: Optional[str] = None
    resource: Optional[Resource]
    action: Optional[Action]

class PermissionGroupSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permission_ids: Optional[List[str]] = []

# ---------------- Output Models ---------------- #

class PermissionObject(BaseModel):
    id: UUID
    resource: Resource
    action: Action

  # <-- allows Pydantic to read from Tortoise ORM models

class PermissionGroupObject(BaseModel):
    id: UUID
    name: str
    permissions: List[PermissionObject] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None



# ---------------- Paginated Responses ---------------- #

class PermissionListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: List[PermissionObject]

class PermissionGroupListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: List[PermissionGroupObject]
