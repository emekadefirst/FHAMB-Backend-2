from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import ContentStatus


class CategorySchema(BaseModel):
    title: Optional[str] = Field(None, max_length=150)


class BlogSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    category_id: Optional[str] = Field(None, max_length=55)
    content: Optional[str] = None
    status: Optional[ContentStatus] = ContentStatus.DRAFT
    tags: Optional[List[str]] = Field(default_factory=list)
    image_ids: Optional[List[str]] = Field(default_factory=list)


