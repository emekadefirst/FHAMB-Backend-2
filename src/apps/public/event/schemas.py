from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import ContentStatus
from datetime import date as dt, time


class EventSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[ContentStatus] = ContentStatus.DRAFT
    venue: Optional[str] = Field(None, max_length=255)
    image_ids: Optional[List[str]] = Field(default_factory=list)  
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class EventDateSchema(BaseModel):
    event_id: Optional[str] = None
    date: Optional[dt] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
