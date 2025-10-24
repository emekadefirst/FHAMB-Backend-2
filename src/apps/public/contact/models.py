from tortoise import fields
from src.utilities.base_model import BaseModel
from tortoise.contrib.postgres.fields import ArrayField


class Social(BaseModel):
    public = fields.BooleanField(default=False)
    name = fields.CharField(255)
    url = fields.CharField(550)

    class Meta:
        table = "social"

class Branch(BaseModel):
    address = fields.TextField()
    hq = fields.BooleanField(default=False)
    phone_numbers: list[str] = ArrayField("text", null=True)
    emails: list[str] = ArrayField("text", null=True)

    class Meta:
        table = "branch"


class ContactUs(BaseModel):
    sender_email = fields.CharField(max_length=55)
    sender_name = fields.CharField(max_length=55)
    body = fields.CharField(max_length=200)
    inquiry_type = fields.CharField(max_length=150, null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    contact_address = fields.TextField(null=True)



    class Meta:
        table = "contact_us"


class Team(BaseModel):
    image = fields.ForeignKeyField("models.File", related_name="team_image", null=True)
    name = fields.CharField(255)
    position = fields.CharField(255)
    about = fields.TextField(null=True)
    rank = fields.IntField(null=True)
    socials = fields.ManyToManyField("models.Social", related_name="team_social")

    class Meta:
        table = "team"
