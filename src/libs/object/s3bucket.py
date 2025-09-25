import aioboto3
from typing import Optional, Mapping, Any, BinaryIO
from src.config.env import (
    S3_BUCKET, AWS_REGION, S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT
)


class AsyncS3:
    def __init__(
        self,
        bucket: str = S3_BUCKET,
        region_name: Optional[str] = AWS_REGION,
        endpoint_url: Optional[str] = S3_ENDPOINT,
        acl: Optional[str] = "public-read",
        aws_access_key_id: Optional[str] = S3_ACCESS_KEY,
        aws_secret_access_key: Optional[str] = S3_SECRET_KEY,
    ):
        self.bucket = bucket
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.acl = acl
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def _build_url(self, key: str) -> str:
        """Helper to return a consistent public URL."""
        if self.endpoint_url:
            base = self.endpoint_url.rstrip("/")
            return f"{base}/{self.bucket}/{key}"
        if self.region_name and self.region_name != "us-east-1":
            return f"https://{self.bucket}.s3.{self.region_name}.amazonaws.com/{key}"
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"

    async def upload_fileobj(
        self,
        fileobj: BinaryIO,
        key: str,
        content_type: Optional[str] = None,
        extra_args: Optional[Mapping[str, Any]] = None,
    ) -> str:
        """Stream upload a file-like object to S3."""
        extra = dict(extra_args or {})
        if content_type:
            extra["ContentType"] = content_type
        if self.acl:
   
            if self.acl.lower() != "public-read":  
                extra["ACL"] = self.acl

        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as s3:
            await s3.upload_fileobj(fileobj, self.bucket, key, ExtraArgs=extra)
        print(self._build_url(key))
        return self._build_url(key)

    async def download_fileobj(self, key: str, fileobj: BinaryIO) -> None:
        """Download an S3 object into a file-like object."""
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as s3:
            await s3.download_fileobj(self.bucket, key, fileobj)

    async def delete_file(self, key: str) -> None:
        """Delete an object from S3."""
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as s3:
            await s3.delete_object(Bucket=self.bucket, Key=key)

    async def generate_presigned_url(
        self,
        key: str,
        expires_in: int = 3600,
        method: str = "get_object"
    ) -> str:
        """Generate a presigned URL for temporary access."""
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as s3:
            url = await s3.generate_presigned_url(
                ClientMethod=method,
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        return url

    async def list_files(self, prefix: Optional[str] = None) -> list[str]:
        """List files in the bucket, optionally filtered by prefix."""
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as s3:
            paginator = s3.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(Bucket=self.bucket, Prefix=prefix or "")
            files = []
            async for page in page_iterator:
                for item in page.get("Contents", []):
                    files.append(item["Key"])
        return files
