from fastapi import BackgroundTasks, Query, Depends
from src.utilities.route_builder import build_router
from src.apps.public.contact.services import SocialService, BranchService, ContactUsService, TeamService
from src.apps.public.contact.schemas import SocialSchema, BranchSchema, ContactUsSchema, TeamSchema

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
async def get_social(id: str):
    return await SocialService.get(id=id)

@social_router.get("/", status_code=200)
async def list_social():
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
async def get_branch(id: str):
    return await BranchService.get(id=id)

@branch_router.get("/", status_code=200)
async def list_branch():
    return await BranchService.all()


# -----------------------------
# ContactUs Router
# -----------------------------
contact_router = build_router(path="contact-us", tags=["ContactUs"])

@contact_router.post(
        "/",
        status_code=201,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.PUBLIC))]        
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
        status_code=200
        )
async def get_contact(id: str):
    return await ContactUsService.get(id=id)

@contact_router.get("/", status_code=200)
async def list_contact():
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

@team_router.get("/{id}")
async def get_team(id: str):
    return await TeamService.get(id=id)

@team_router.get("/")
async def list_team():
    return await TeamService.all()
