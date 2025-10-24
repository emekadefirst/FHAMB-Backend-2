from fastapi import Depends, Query, Request
from src.utilities.route_builder import build_router
from src.apps.public.blog.services import BlogService, CategoryService
from src.utilities.crypto import JWTService
from src.apps.public.blog.schemas import CategorySchema, BlogSchema
from src.apps.auth.user import User
from src.core.cache import cache
from src.enums.base import Action, Resource
from uuid import UUID
from src.dependencies.permissions.base import AuthPermissionService

category_router = build_router(path="categories", tags=["Categories"])
blogs_router = build_router(path="blogs", tags=["Blogs"])
jwt = JWTService()

# =======================
# CATEGORY ROUTES
# =======================

@category_router.get("/", status_code=200)
# @cache(ttl=600)  # ✅ Cache for 10 minutes (categories rarely change)
async def get_categories(request: Request):
    return await CategoryService.all()


@category_router.get("/{id}", status_code=200)
# @cache(ttl=600)  # ✅ Cache for 10 minutes per category
async def get_category(id: str, request: Request):
    return await CategoryService.get(id)


@category_router.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_category(dto: CategorySchema, user: User = Depends(jwt.get_current_user)):
    return await CategoryService.create(user=user, dto=dto)


@category_router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_category(id: str, dto: CategorySchema):
    return await CategoryService.update(id=id, dto=dto)


@category_router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.PUBLIC))]
)
async def delete_category(id: str):
    return await CategoryService.delete(id=id)


# =======================
# BLOG ROUTES
# =======================

@blogs_router.get("/", status_code=200)
# @cache(ttl=300)  # ✅ Cache for 5 minutes (blog lists change more often)
async def list_blogs(request: Request, author: str = Query(None), category: str = Query(None)):
    return await BlogService.all(author=author, category=category)


@blogs_router.get("/{slug_or_id}", status_code=200)
# @cache(ttl=600)  # ✅ Cache for 10 minutes per blog post
async def get_blog(slug_or_id: str, request: Request):
    try:
        UUID(slug_or_id)
        return await BlogService.get(id=slug_or_id)
    except ValueError:
        return await BlogService.get(slug=slug_or_id)


@blogs_router.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_blog(dto: BlogSchema, user: User = Depends(jwt.get_current_user)):
    return await BlogService.create(user=user, dto=dto)


@blogs_router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_blog(id: str, dto: BlogSchema):
    return await BlogService.update(id=id, dto=dto)


@blogs_router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.PUBLIC))]
)
async def delete_blog(id: str):
    return await BlogService.delete(id=id)
