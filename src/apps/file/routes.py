from fastapi import UploadFile, Depends
from src.utilities.route_builder import build_router
from src.apps.file.services import S3FileService, CloudinaryFileService, FileService

from src.enums.base import Action, Resource
from src.dependencies.permissions.base import AuthPermissionService


file_router = build_router(path="file", tags=["File"])


@file_router.post(
        "/upload/s3",
        status_code=201,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.FILE))]
        )
async def upload_to_s3(file: UploadFile):
    return await S3FileService.add(file)


@file_router.post(
        "/upload/cloudinary",
        status_code=201,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.CREATE, resource=Resource.FILE))]
        )
async def upload_to_cloudinary(file: UploadFile):
    return await CloudinaryFileService.upload(file)


@file_router.get(
        "/list",
        status_code=200,
        dependencies=[Depends(AuthPermissionService.permission_required(action=Action.READ, resource=Resource.FILE))]
        )
async def list_files():
    return await FileService.list()

