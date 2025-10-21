from fastapi import APIRouter
from src.apps.public.faq.schema import FAQSchema
from src.apps.public.faq.service import FAQService

faq_router = APIRouter(prefix="/faqs", tags=["FAQs"])


@faq_router.post("/", status_code=201)
async def create_faq(dto: FAQSchema):
    return await FAQService.create(dto=dto)


@faq_router.get("/", status_code=200)
async def list_faqs(author: str | None = None, category: str | None = None):
    return await FAQService.all(author=author, category=category)

@faq_router.get("/{id}", status_code=200)
async def get_faq(id: str):
    return await FAQService.get(id=id)


@faq_router.patch("/{id}", status_code=200)
async def update_faq(id: str, dto: FAQSchema):
    return await FAQService.update(id=id, dto=dto)


@faq_router.delete("/{id}", status_code=200)
async def delete_faq(id: str):
    return await FAQService.delete(id=id)
