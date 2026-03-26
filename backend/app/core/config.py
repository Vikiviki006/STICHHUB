"""
StitchHub — Core Configuration
All settings loaded from environment variables / .env file
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "postgresql://stitchhub:stitchhub@localhost:5432/stitchhub"

    # AWS S3 (for dress images + 3D models)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "stitchhub-assets"

    # Email (SendGrid)
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@stitchhub.com"

    # Shipping
    FEDEX_API_KEY: str = ""
    FEDEX_SECRET_KEY: str = ""
    FEDEX_ACCOUNT_NUMBER: str = ""
    DHL_API_KEY: str = ""
    DHL_API_SECRET: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "https://stitchhub.com"]
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()