import hashlib
import time
import mimetypes
import uuid
import orjson
from typing import Union, IO
import httpx
from fastapi import UploadFile
from src.config.env import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME


def sign(params: dict, secret: str) -> str:
    """Generate Cloudinary API signature (SHA1)."""
    sorted_params = sorted((k, v) for k, v in params.items() if v is not None)
    query = "&".join(f"{k}={v}" for k, v in sorted_params)
    to_sign = f"{query}{secret}"
    return hashlib.sha1(to_sign.encode("utf-8")).hexdigest()


class CloudinaryService:
    DOMAIN = "https://api.cloudinary.com"
    PATH = f"/v1_1/{CLOUDINARY_CLOUD_NAME}"

    @classmethod
    async def upload(cls, file: UploadFile, resource_type: str = "auto") -> str:
        timestamp = int(time.time())
        params = {"timestamp": timestamp}
        signature = sign(params, CLOUDINARY_API_SECRET)

        fields = {
            "timestamp": str(timestamp),
            "api_key": CLOUDINARY_API_KEY,
            "signature": signature,
        }

        filename = file.filename or f"upload-{uuid.uuid4().hex}.bin"
        mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        url = f"{cls.DOMAIN}{cls.PATH}/{resource_type}/upload"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                url,
                data=fields,
                files={  
                    "file": (filename, file.file, mimetype)
                },
            )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Cloudinary upload failed: {resp.status_code} {resp.text}"
            )

        result = orjson.loads(resp.content)
        return result["secure_url"]
