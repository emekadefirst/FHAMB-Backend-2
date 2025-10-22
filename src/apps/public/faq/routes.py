from fastapi import APIRouter, Depends
from src.utilities.route_builder import build_router
from src.apps.public.faq.schema import FAQSchema
from src.apps.public.faq.service import FAQService
from src.core.cache import cache


faq_router = build_router(path="faqs", tags=["FAQs"])


from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService



@faq_router.post(
        "/", 
        status_code=201,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
        )
async def create_faq(dto: FAQSchema):
    return await FAQService.create(dto=dto)

@cache(ttl=120)
@faq_router.get(
        "/", 
        status_code=200
        )
async def list_faqs(author: str | None = None, category: str | None = None):
    return await FAQService.all(author=author, category=category)

@cache(ttl=120)
@faq_router.get("/{id}", status_code=200)
async def get_faq(id: str):
    return await FAQService.get(id=id)


@faq_router.patch(
        "/{id}", 
        status_code=200,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
        )
async def update_faq(id: str, dto: FAQSchema):
    return await FAQService.update(id=id, dto=dto)


@faq_router.delete(
        "/{id}", 
        status_code=204,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.PUBLIC))]
        )
async def delete_faq(id: str):
    return await FAQService.delete(id=id)
