from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import ContentStatus


class GallerySchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category_id: Optional[str] = Field(None, description="ID of the gallery category")
    author_id: Optional[str] = Field(None, description="ID of the user creating the gallery")
    status: Optional[ContentStatus] = ContentStatus.DRAFT
    image_ids: Optional[List[str]] = Field(default_factory=list)
