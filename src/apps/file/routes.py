from fastapi import UploadFile, HTTPException
from src.utilities.route_builder import build_router
from src.apps.file.services import S3FileService, CloudinaryFileService, FileService

file_router = build_router(path="file", tags=["File"])


@file_router.post("/upload/s3")
async def upload_to_s3(file: UploadFile):
    return await S3FileService.add(file)


@file_router.post("/upload/cloudinary")
async def upload_to_cloudinary(file: UploadFile):
    return await CloudinaryFileService.upload(file)


@file_router.get("/list")
async def list_files():
    return await FileService.list()

