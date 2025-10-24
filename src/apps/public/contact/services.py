from fastapi import BackgroundTasks
from typing import List, Optional
from src.utilities.base_service import BaseObjectService
from src.libs.smtp.mailer import EmailService
from src.libs.smtp.templates.contactus import contact
from src.apps.public.contact import Social, Branch, ContactUs, Team
from src.error.base import ErrorHandler
from src.apps.file.models import File
from tortoise.queryset import QuerySet
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
        data_dict = dto.dict(exclude={"image_id", "socials"})

        image = await cls.file.model.get_or_none(id=dto.image_id)
        if not image:
            raise cls.error.get(404, "Image not found")

        # ✅ Create team with image set immediately
        team = await cls.boa.model.create(**data_dict, image=image)

        # ✅ Handle socials (create or link)
        if dto.socials:
            social_objs = []
            for social in dto.socials:
                obj, _ = await Social.get_or_create(**social.dict())
                social_objs.append(obj)
            await team.socials.add(*social_objs)

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
        obj = await cls.boa.model.filter(**filters).prefetch_related("socials").select_related("image").first()
        if not obj:
            raise cls.error(404)


        socials = await obj.socials.all()

        return {
            "id": str(obj.id),
            "name": obj.name,
            "position": obj.position,
            "about": obj.about,
            "rank": obj.rank,
            "image": obj.image.url if obj.image else None,
            "socials": [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "url": s.url,
                    "public": s.public,
                }
                for s in socials
            ],
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }



    @classmethod
    async def all(
        cls,
        page: int = 1,
        page_size: int = 10,
        prefetch: Optional[List[str]] = None,
        select: Optional[List[str]] = None,
    ):
        query: QuerySet = cls.boa.model.filter(is_deleted=False)
        if prefetch:
            query = query.prefetch_related(*prefetch)
        else:
            query = query.prefetch_related("socials")

        if select:
            query = query.select_related(*select)
        else:
            query = query.select_related("image")

        total = await query.count()
        teams = await query.offset((page - 1) * page_size).limit(page_size)

        results = []
        for team in teams:
            socials = await cls.social_boa.model.all()
            results.append({
                "id": str(team.id),
                "name": team.name,
                "position": team.position,
                "about": team.about,
                "rank": team.rank,
                "image": team.image.url if team.image else None,
                "socials": [
                    {
                        "id": str(s.id),
                        "name": s.name,
                        "url": s.url,
                        "public": s.public,
                    }
                    for s in socials
                ],
                "created_at": team.created_at,
                "updated_at": team.updated_at,
            })

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "data": results,
        }


    @classmethod
    async def delete(cls, id: str):
        return await cls.boa.trash(id=id)
    

