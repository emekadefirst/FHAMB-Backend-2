from fastapi import Depends, Query
from src.utilities.route_builder import build_router
from src.apps.public.gallery.schema import GallerySchema
from src.apps.public.gallery.service import GalleryService

gallery_router = build_router(path="/galleries", tags=["Galleries"])

 
from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService


@gallery_router.post(
        "/", 
        status_code=201,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
        )
async def create_gallery(dto: GallerySchema):
    return await GalleryService.create(dto=dto)


@gallery_router.get(
        "/", 
        status_code=200
        )
async def list_galleries(
    author: str | None = None, 
    category: str | None = None
    ):
    return await GalleryService.all(author=author, category=category)

@gallery_router.get(
        "/{id}", 
        status_code=200
        )
async def get_gallery(id: str):
    return await GalleryService.get(id=id)

@gallery_router.patch(
        "/{id}", 
        status_code=200,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
        )
async def update_gallery(id: str, dto: GallerySchema):
    return await GalleryService.update(id=id, dto=dto)

@gallery_router.delete(
        "/{id}", 
        status_code=204,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.PUBLIC))]
        )
async def delete_gallery(id: str):
    return await GalleryService.delete(id=id)

@gallery_router.get("/search/", status_code=200)
async def search_galleries(q: str = Query(..., description="Search galleries by keyword")):
    return await GalleryService.search(query=q)
