import os
import re
import time
import secrets
import mimetypes
from fastapi import UploadFile, HTTPException
from src.libs.object.s3bucket import AsyncS3
from src.libs.object.cloudinary import CloudinaryService
from src.apps.file.models import File
from src.utilities.base_service import BaseObjectService
from src.utilities.sanitizer import detect_type, SUPPORTED_FILE_TYPES, detect_type, EXTENSION_MAP, scan_pdf_for_malware_bytes 
from src.enums.base import FileType
from typing import Optional, List

def slugify(name: str) -> str:
    base = os.path.splitext(name)[0]
    base = re.sub(r"[^a-zA-Z0-9\-_.]+", "-", base).strip("-._").lower()
    suffix = secrets.token_hex(4) 
    return f"{base}-{suffix}" if base else suffix

def map_filetype_from_mime(content_type: Optional[str]) -> FileType:
    if not content_type:
        return FileType.DOCUMENT 
    ct = content_type.lower()
    if ct.startswith("image/"):
        return FileType.IMAGE
    if ct.startswith("video/"):
        return FileType.VIDEO
    if ct.startswith("audio/"):
        return FileType.AUDIO
    return FileType.DOCUMENT


class S3FileService:
    def __init__(self,  key_prefix: str = "uploads/"):
        self.s3 = AsyncS3()
        self.key_prefix = key_prefix.rstrip("/") + "/"

    @staticmethod
    async def list():
        return await File.filter(is_deleted=False)

    @staticmethod
    async def get(id: str):
        file = await File.get_or_none(id=id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        return file

    async def add(self, file: UploadFile):

        HEAD = 64 * 1024
        head = await file.read(HEAD)
        await file.seek(0)
        filename = file.filename or "upload"
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext not in SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported extension {ext}")

        need_full = ext in {".pdf", ".docx", ".xlsx", ".pptx"}
        full_bytes = None

        sig = detect_type(head, None)  
        if (sig == "zip" and ext in {".docx", ".xlsx", ".pptx"}) or need_full:
            full_bytes = await file.read()   
            await file.seek(0)
            sig = detect_type(full_bytes[:HEAD], full_bytes) 

        if not sig:
            raise HTTPException(status_code=400, detail="Unknown file type (signature not recognized)")

        valid_exts = EXTENSION_MAP.get(sig, [])
        if ext.lstrip(".") not in valid_exts:
            raise HTTPException(status_code=400, detail=f"Mismatch: extension {ext} vs signature {sig}")

        if sig == "pdf":
            if full_bytes is None:
                full_bytes = await file.read()
                await file.seek(0)
            scan = scan_pdf_for_malware_bytes(full_bytes)
            if scan is not True:
                raise HTTPException(status_code=400, detail=f"PDF blocked: {scan}")
        try:
            pos = file.file.tell()
        except Exception:
            pos = 0
        try:
            file.file.seek(0, 2) 
            size = file.file.tell()
            file.file.seek(0)      
        except Exception:
            size = len(full_bytes) if full_bytes is not None else len(head)

        ftype = map_filetype_from_mime(file.content_type)
        now = int(time.time())
        slug = slugify(filename)
        key = f"{self.key_prefix}{now}/{slug}{ext}"
        try:
            puburl = await self.s3.upload_fileobj(
                fileobj=file.file,  
                key=key,
                content_type=file.content_type or "application/octet-stream",
                extra_args=None,
            )
            public_url = await self._build_public_url(key)
        finally:
            try:
                file.file.seek(0)
            except Exception:
                pass

        new_file = await File.create(
            name=os.path.splitext(filename)[0],
            size=size,
            url=puburl,
            slug=slug,
            extension=ext.lstrip("."),
            type=ftype,
            meta_signature=sig,
        )
        return new_file

    async def _build_public_url(self, key: str) -> str:
        # We already return URL from AsyncS3.upload_fileobj, but keeping a hook if you want custom CDN domain later.
        # (You can collapse this and just return the upload_fileobj result.)
        # For now, re-derive it from the S3 client for clarity:
        # NOTE: you can store/return a CDN URL here if fronted by CloudFront.
        return ""  # not used; we returned the URL directly in upload_fileobj



    



class CloudinaryFileService:
    boa = BaseObjectService(File)
    bucket = CloudinaryService
    model = File

    @classmethod
    async def upload(cls, file: Optional[UploadFile], user_id: Optional[str] = None) -> File:
        if not file:
            raise cls.error.get(400, "No files provided")

        url = await cls.bucket.upload(file)
        filename, ext = os.path.splitext(file.filename)
        ext = ext.replace(".", "").lower()
        mime_type = mimetypes.guess_type(file.filename)[0]

        file_data = {
            "name": filename,
            "slug": filename.replace(" ", "_").lower(),
            "extension": ext,
            "mime_type": mime_type,
            "url": url,
            "size": file.size,
            "user_id": user_id,
            "type": cls._get_file_type(ext),
        }

        file_obj = cls.model(**file_data)
        await file_obj.save()
        return file_obj


    @classmethod
    def _get_file_type(cls, ext: str) -> str:
        from src.enums.base import ImageExtension, VideoExtension, DocumentExtension, AudioExtension, FileType

        if ext in ImageExtension._value2member_map_:
            return FileType.IMAGE
        if ext in VideoExtension._value2member_map_:
            return FileType.VIDEO
        if ext in DocumentExtension._value2member_map_:
            return FileType.DOCUMENT
        if ext in AudioExtension._value2member_map_:
            return FileType.AUDIO
        return FileType.DOCUMENT  



class FileService:
    boa = BaseObjectService(File)

    @classmethod
    async def list(cls):
        """List all non-deleted files"""
        return await cls.boa.all()
