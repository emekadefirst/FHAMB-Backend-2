from fastapi import APIRouter, Query
from src.apps.public.gallery.schema import GallerySchema
from src.apps.public.gallery.service import GalleryService

gallery_router = APIRouter(prefix="/galleries", tags=["Galleries"])

@gallery_router.post("/", status_code=201)
async def create_gallery(dto: GallerySchema):
    return await GalleryService.create(dto=dto)


@gallery_router.get("/", status_code=200)
async def list_galleries(author: str | None = None, category: str | None = None):
    return await GalleryService.all(author=author, category=category)

@gallery_router.get("/{id}", status_code=200)
async def get_gallery(id: str):
    return await GalleryService.get(id=id)

@gallery_router.patch("/{id}", status_code=200)
async def update_gallery(id: str, dto: GallerySchema):
    return await GalleryService.update(id=id, dto=dto)

@gallery_router.delete("/{id}", status_code=200)
async def delete_gallery(id: str):
    return await GalleryService.delete(id=id)

@gallery_router.get("/search/", status_code=200)
async def search_galleries(q: str = Query(..., description="Search galleries by keyword")):
    return await GalleryService.search(query=q)
