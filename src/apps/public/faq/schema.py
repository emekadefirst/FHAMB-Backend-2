from pydantic import BaseModel, Field
from typing import Optional
from src.enums.base import ContentStatus


class FAQSchema(BaseModel):
    question: Optional[str] = Field(None, max_length=500)
    answer: Optional[str] = None
    author_id: Optional[str] = Field(None, max_length=65)
    status: Optional[ContentStatus] = ContentStatus.DRAFT
    category_id: Optional[str] = Field(None, max_length=65)
