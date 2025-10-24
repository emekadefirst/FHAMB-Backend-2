from fastapi import BackgroundTasks, Query, Depends, Request
from src.utilities.route_builder import build_router
from src.apps.public.contact.services import SocialService, BranchService, ContactUsService, TeamService
from src.apps.public.contact.schemas import SocialSchema, BranchSchema, ContactUsSchema, TeamSchema
from src.core.cache import cache
from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService

# -----------------------------
# Social Router
# -----------------------------
social_router = build_router(path="social", tags=["Social"])

@social_router.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_social(data: SocialSchema):
    return await SocialService.create(data)

@social_router.patch(
    "/{id}",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_social(id: str, data: SocialSchema):
    return await SocialService.update(id, data)

@social_router.get("/{id}", status_code=200)
# @cache(ttl=900)  # ✅ Cache 15 minutes for individual social record
async def get_social(id: str, request: Request):
    return await SocialService.get(id=id)

@social_router.get("/", status_code=200)
# @cache(ttl=900)  # ✅ Cache 15 minutes for all social links
async def list_social(request: Request):
    return await SocialService.all()


# -----------------------------
# Branch Router
# -----------------------------
branch_router = build_router(path="branch", tags=["Branch"])

@branch_router.post(
    "/",
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_branch(data: BranchSchema):
    return await BranchService.create(data)

@branch_router.patch(
    "/{id}",
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_branch(id: str, data: BranchSchema):
    return await BranchService.update(id, data)

@branch_router.get("/{id}", status_code=200)
# @cache(ttl=1800)  # ✅ Cache 30 minutes (branch details rarely change)
async def get_branch(id: str, request: Request):
    return await BranchService.get(id=id)

@branch_router.get("/", status_code=200)
# @cache(ttl=1800)  # ✅ Cache 30 minutes (list of branches)
async def list_branch(request: Request):
    return await BranchService.all()


# -----------------------------
# ContactUs Router
# -----------------------------
contact_router = build_router(path="contact-us", tags=["ContactUs"])

@contact_router.post(
    "/",
    status_code=201
)
async def create_contact(data: ContactUsSchema, background_tasks: BackgroundTasks):
    return await ContactUsService.create(data, background_tasks)

@contact_router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_contact(id: str, data: ContactUsSchema):
    return await ContactUsService.update(id, data)

@contact_router.get(
        "/{id}", 
        status_code=200,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
        )
# @cache(ttl=900)  # ✅ Cache 15 minutes
async def get_contact(id: str, request: Request):
    return await ContactUsService.get(id=id)

@contact_router.get(
        "/", 
        status_code=200,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.PUBLIC))]
        )
# @cache(ttl=900)  # ✅ Cache 15 minutes (list of contact requests)
async def list_contact(request: Request):
    return await ContactUsService.all()


# -----------------------------
# Team Router
# -----------------------------
team_router = build_router(path="team", tags=["Team"])

@team_router.post(
    "/", 
    status_code=201,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]
)
async def create_team(data: TeamSchema):
    return await TeamService.create(data)

@team_router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.UPDATE, resource=Resource.PUBLIC))]
)
async def update_team(id: str, data: TeamSchema):
    return await TeamService.update(id, data)

@team_router.get("/{id}", status_code=200)
# @cache(ttl=900)  # ✅ Cache 15 minutes per team member
async def get_team(id: str, request: Request):
    return await TeamService.get(id=id)

@team_router.get("/", status_code=200)
# @cache(ttl=900)  # ✅ Uncomment if you want caching for 15 mins
async def list_team(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
):

    return await TeamService.all(page=page, page_size=page_size)


@team_router.delete(
    "/{id}", 
    status_code=204,
    dependencies=[Depends(AuthPermissionService.permission_required(action=Action.DELETE, resource=Resource.PUBLIC))]
    )
async def delete_team(id: str):
    return await TeamService.delete(id=id)