from fastapi import BackgroundTasks
from typing import List, Optional
from src.utilities.base_service import BaseObjectService
from src.libs.smtp.mailer import EmailService
from src.libs.smtp.templates.contactus import contact
from src.apps.public.contact import Social, Branch, ContactUs, Team
from src.error.base import ErrorHandler
from src.apps.file.models import File
from src.apps.public.contact.schemas import ContactUsSchema, TeamSchema, BranchSchema, SocialSchema


class SocialService:
    boa = BaseObjectService(Social)
    error = ErrorHandler(Social)

    @classmethod
    async def create(cls, dto: SocialSchema):
        return await cls.boa.model.create(**dto.dict())

    @classmethod
    async def update(cls, id: str, dto: SocialSchema):
        obj = await cls.boa.get_object_or_404(id=id)
        if not obj:
            raise cls.error.get(404)
        for field, value in dto.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @classmethod
    async def get(cls, **filters):
        obj = await cls.boa.get_object_or_404(**filters)
        if not obj:
            raise cls.error.get(404)
        return obj

    @classmethod
    async def all(cls, prefetch: Optional[List[str]] = None, select: Optional[List[str]] = None):
        return await cls.boa.all(prefetch_related=prefetch, select_related=select)


class BranchService:
    boa = BaseObjectService(Branch)
    error = ErrorHandler(Branch)

    @classmethod
    async def create(cls, dto: BranchSchema):
        return await cls.boa.model.create(**dto.dict())

    @classmethod
    async def update(cls, id: str, dto: BranchSchema):
        obj = await cls.boa.get_object_or_404(id=id)
        if not obj:
            raise cls.error.get(404)
        for field, value in dto.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @classmethod
    async def get(cls, **filters):
        obj = await cls.boa.get_object_or_404(**filters)
        if not obj:
            raise cls.error.get(404)
        return obj

    @classmethod
    async def all(cls, prefetch: Optional[List[str]] = None, select: Optional[List[str]] = None):
        return await cls.boa.all(prefetch_related=prefetch, select_related=select)


class ContactUsService:
    boa = BaseObjectService(ContactUs)
    error = ErrorHandler(ContactUs)
    smtp = EmailService()

    @classmethod
    async def create(cls, dto: ContactUsSchema, background_tasks: BackgroundTasks):
        contact_obj = await cls.boa.model.create(**dto.dict())

        body = contact(dto.sender_name)
        background_tasks.add_task(
            cls.smtp.send_email,
            subject=f"{dto.inquiry_type} {dto.phone_number}",
            body=dto.body,
            to_emails=["info@fhamortgage.gov.ng"]
        )
        background_tasks.add_task(
            cls.smtp.send_email,
            subject="Thank you for contacting us",
            body=body,
            to_emails=[dto.sender_email]
        )
        return contact_obj

    @classmethod
    async def update(cls, id: str, dto: ContactUsSchema):
        obj = await cls.boa.get_object_or_404(id=id)
        if not obj:
            raise cls.error.get(404)
        for field, value in dto.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @classmethod
    async def get(cls, **filters):
        obj = await cls.boa.get_object_or_404(**filters)
        if not obj:
            raise cls.error.get(404)
        return obj

    @classmethod
    async def all(cls):
        return await cls.boa.all()


class TeamService:
    boa = BaseObjectService(Team)
    error = ErrorHandler(Team)
    file = BaseObjectService(File)
    social_boa = BaseObjectService(Social)

    @classmethod
    async def create(cls, dto: TeamSchema):
        # Convert to dict but exclude M2M and FK
        data_dict = dto.dict(exclude={"image_id", "socials"})

        # Create base team
        team = await cls.boa.model.create(**data_dict)

        # Attach image (FK)
        if dto.image_id:
            image = await cls.file.model.get_or_none(id=dto.image_id)
            if image:
                team.image = image
                await team.save()

        # Handle ManyToMany socials
        if dto.socials:
            for social_data in dto.socials:
                # Check if a social with the same name/url exists
                existing_social = await cls.social_boa.model.get_or_none(
                    name=social_data.name, url=social_data.url
                )
                if existing_social:
                    await team.socials.add(existing_social)
                else:
                    new_social = await cls.social_boa.model.create(**social_data.dict())
                    await team.socials.add(new_social)

        return team

    @classmethod
    async def update(cls, id: str, dto: TeamSchema):
        obj = await cls.boa.get_object_or_404(id=id)
        if not obj:
            raise cls.error.get(404)

        update_data = dto.dict(exclude_unset=True, exclude={"socials", "image_id"})

        # Update base fields
        for field, value in update_data.items():
            setattr(obj, field, value)
        await obj.save()

        # Update image if provided
        if dto.image_id:
            image = await cls.file.model.get_or_none(id=dto.image_id)
            if image:
                obj.image = image
                await obj.save()

        # Update socials if provided
        if dto.socials is not None:
            await obj.socials.clear()  # Remove all existing
            for social_data in dto.socials:
                existing_social = await cls.social_boa.model.get_or_none(
                    name=social_data.name, url=social_data.url
                )
                if existing_social:
                    await obj.socials.add(existing_social)
                else:
                    new_social = await cls.social_boa.model.create(**social_data.dict())
                    await obj.socials.add(new_social)

        return obj

    @classmethod
    async def get(cls, **filters):
        obj = await cls.boa.get_object_or_404(**filters)
        if not obj:
            raise cls.error.get(404)
        return obj

    @classmethod
    async def all(cls, prefetch: Optional[List[str]] = None, select: Optional[List[str]] = None):
        # Prefetch socials and image if not specified
        prefetch = prefetch or ["socials", "image"]
        return await cls.boa.all(prefetch_related=prefetch, select_related=select)
