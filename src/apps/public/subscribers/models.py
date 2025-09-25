from src.utilities.base_model import BaseModel
from tortoise import fields



class Subscriber(BaseModel):
    email = fields.CharField(255, unique=True)


    class Meta:
        table = "subscribers"