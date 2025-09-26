from pydantic import BaseModel, Field, EmailStr

class SubscriberSchema(BaseModel):
    email: EmailStr