from pydantic import EmailStr, BaseModel, Field
from typing import Optional, List
from src.enums.base import EmailCategory

class EmailSchema(BaseModel):
    sender: EmailStr
    subject: Optional[str] = Field(None, max_length=225)
    recipients: Optional[List[EmailStr]]
    body: Optional[str]
    attachments: Optional[List[str]] =  [] 
    category: Optional[EmailCategory] = EmailCategory.TRANSACTIONAL
