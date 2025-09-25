from src.utilities.base_model import BaseModel
from tortoise import fields
from src.enums.base import EmailCategory, EmailStatus


class Email(BaseModel):
    sender = fields.CharField(max_length=255)
    subject = fields.CharField(max_length=255)
    recipients = fields.JSONField()
    body = fields.TextField()
    attachments = fields.ManyToManyField("models.File", related_name="emails")
    status = fields.CharEnumField(EmailStatus, default=EmailStatus.PENDING)
    category = fields.CharEnumField(EmailCategory, default=EmailCategory.NOTIFICATION)



    class Meta:
        table = "mail_email"
