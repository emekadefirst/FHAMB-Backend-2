import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

AWS_REGION = str(os.getenv('AWS_REGION'))

JWT_ACCESS_EXPIRY = int(os.getenv('JWT_ACCESS_EXPIRY'))
JWT_REFRESH_EXPIRY = int(os.getenv('JWT_REFRESH_EXPIRY'))
JWT_ACCESS_SECRET = str(os.getenv('JWT_ACCESS_SECRET'))
JWT_ALGORITHM = str(os.getenv('JWT_ALGORITHM'))
ENCRYPTION_KEY = str(os.getenv('ENCRYPTION_KEY'))

ENCRYPTION_KEY = str(os.getenv('ENCRYPTION_KEY'))

DB_NAME = str(os.getenv('DB_NAME'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = str(os.getenv('DB_USER'))

TEST_DATABASE_URL = str(os.getenv('TEST_DATABASE_URL'))

S3_ACCESS_KEY = str(os.getenv('S3_ACCESS_KEY'))
S3_SECRET_KEY = str(os.getenv('S3_SECRET_KEY'))
S3_ENDPOINT = str(os.getenv('S3_ENDPOINT'))
S3_BUCKET = str(os.getenv('S3_BUCKET'))

CLOUDINARY_CLOUD_NAME = str(os.getenv('CLOUDINARY_CLOUD_NAME'))
CLOUDINARY_API_KEY = str(os.getenv('CLOUDINARY_API_KEY'))
CLOUDINARY_API_SECRET = str(os.getenv('CLOUDINARY_API_SECRET'))
CLOUDINARY_URL = str(os.getenv('CLOUDINARY_URL'))

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = str(os.getenv("EMAIL_USER"))
EMAIL_PASSWORD = str(os.getenv("EMAIL_PASSWORD"))

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
