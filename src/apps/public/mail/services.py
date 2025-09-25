from fastapi import BackgroundTasks
from tortoise.expressions import Q
from src.apps.public.mail import Email
from src.utilities.base_service import BaseObjectService
from src.libs.smtp.mailer import EmailService
from src.apps.file import File
import asyncio
from src.apps.public.mail.schemas import EmailSchema
from src.libs.smtp.templates.message import send_mail


class EmailRouteService:
    smtp = EmailService()
    boa = BaseObjectService(Email)
    file = BaseObjectService(File)

    @classmethod
    async def create_mail(cls, dto: EmailSchema, task: BackgroundTasks):
        data_dict = dto.model_dump(exclude={"attachments"})
        mail = await cls.boa.model.create(**data_dict)

        if dto.attachments:
            files = []
            for att_id in dto.attachments:
                attachment = await cls.file.get_object_or_404(id=att_id)
                files.append(attachment)
            await mail.attachments.add(*files)

        # fire-and-forget email send
        asyncio.create_task(
            cls.smtp.send_email(
                subject=dto.subject,
                body=send_mail(dto.body),
                to_emails=dto.recipients,
                from_email=dto.sender
            )
        )
        return mail

    @classmethod
    async def all_mail(cls, limit: int = 50, offset: int = 0):
        return (
            await cls.boa.model.all()
            .order_by("-created_at")
            .offset(offset)
            .limit(limit)
        )

    @classmethod
    async def search_mail(cls, query: str, limit: int = 50, offset: int = 0):
        """
        Search emails by subject, body, sender, or recipients.
        """
        return (
            await cls.boa.model.filter(
                Q(subject__icontains=query)
                | Q(body__icontains=query)
                | Q(sender__icontains=query)
                | Q(recipients__icontains=query)
            )
            .order_by("-created_at")
            .offset(offset)
            .limit(limit)
        )



