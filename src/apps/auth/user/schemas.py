from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class UserCreateDto(BaseModel):
    email: EmailStr 
    password: str 
    first_name: Optional[str] = Field(max_length=55, description="User's first name")
    last_name: Optional[str] = Field(max_length=55, description="User's last name") 
    other_name: Optional[str] = Field(max_length=55, description="User's other name")
    contact_address: Optional[str] = None
    profile_picture_id: Optional[str] = None
    has_agreed_to_terms: bool
    phone_number: Optional[str] = Field(
        default=None,
        description="Phone number associated with the user",
        max_length=15,
        min_length=10
    )
    latitude: Optional[float] = None
    longitude: Optional[float]= None
    device_id: Optional[str]= None


class UserObjectDto(BaseModel):
    id: UUID
    email: EmailStr 
    first_name: str
    last_name: str
    other_name: str
    contact_address: str 
    has_agreed_to_terms: bool
    phone_number: str
    is_staff: bool
    is_verified: bool
    is_superuser: bool
    profile_picture: str
    latitude: str 
    longitude: str
    last_login: datetime

    class Config:
            from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    latitude: Optional[float] = None
    longitude: Optional[float]= None
    device_id: Optional[str]= None


class RefreshRequest(BaseModel):
    refresh_token: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(max_length=55, description="User's first name")
    last_name: Optional[str] = Field(max_length=55, description="User's last name")
    other_name: Optional[str] = Field(max_length=55, description="User's other name")


class RequestReset(BaseModel):
    email: EmailStr

class VerifyRequestDto(BaseModel):
    email: EmailStr
    otp: str

class UpdatePasswordDto(BaseModel):
    email: EmailStr
    otp: str
    newpassword: str