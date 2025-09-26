from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class SocialSchema(BaseModel):
    public: Optional[bool] = False
    name: str = Field(..., max_length=255)
    url: str = Field(..., max_length=550)

    class Config:
        orm_mode = True


class BranchSchema(BaseModel):
    address: Optional[str] = None
    hq: Optional[bool] = False
    phone_numbers: Optional[List[str]] = []
    emails: Optional[List[str]] = []

    class Config:
        orm_mode = True


class ContactUsSchema(BaseModel):
    sender_email: EmailStr
    sender_name: Optional[str] = Field(..., max_length=255)
    body: Optional[str] = None
    inquiry_type: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    contact_address: Optional[str] = None

    class Config:
        orm_mode = True


class TeamSchema(BaseModel):
    image_id: Optional[str] = None  # Reference to File model
    name: Optional[str] = Field(..., max_length=255)
    position: Optional[str] = Field(..., max_length=255)
    about: Optional[str] = None
    rank: Optional[int] = None
    socials: Optional[List[SocialSchema]] = []

    class Config:
        orm_mode = True
