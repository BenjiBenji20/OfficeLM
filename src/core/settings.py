from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core Application Settings
    APP_NAME: str = "OfficeLM System"
    DEBUG: bool = True
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"
    LOG_LEVEL: str = "INFO"
    DEPLOYMENT_MODE: str = "cloud"

    # Security Headers
    SECRET_HEADER_NAME: str | None = None
    SECRET_HEADER_VALUE: str | None = None

    # API Documentation
    API_DOCS_URL: str | None = None
    API_REDOC_URL: str | None = None
    OPENAPI_URL: str | None = None

    # Database Settings - Staging
    POSTGRES_STAGING_USER: str | None = None
    POSTGRES_STAGING_PASSWORD: str | None = None
    POSTGRES_STAGING_DB: str | None = None
    DATABASE_URL: str | None = None

    # Database Settings - Test
    POSTGRES_TEST_USER: str | None = None
    POSTGRES_TEST_PASSWORD: str | None = None
    POSTGRES_TEST_DB: str | None = None
    TEST_DATABASE_URL: str | None = None
    DB_IO_SESSION_THROTTLING_TIME_S: int = 300

    # Redis Settings - Staging
    REDIS_STAGING_PASSWORD: str | None = None
    REDIS_URL: str | None = None

    # Redis Settings - Test
    REDIS_TEST_PASSWORD: str | None = None
    TEST_REDIS_URL: str | None = None

    # JWT Settings
    ACCESS_JWT_SECRET_KEY: str | None = None
    REFRESH_JWT_SECRET_KEY: str | None = None
    ACCESS_JWT_EXPIRY_SEC: int = 900
    REFRESH_JWT_EXPIRY_SEC: int = 604800
    JWT_ALGORITHM: str = "HS256"

    # Cookie Settings
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"

    # Initial Admin Seed Settings
    SEED_SUPERADMIN_USERNAME: str = "superadmin"
    SEED_SUPERADMIN_EMAIL: str = "admin@system.local"
    SEED_SUPERADMIN_PASSWORD: str = "Admin@123456"

    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL or ""
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        if "?schema=" in url:
            url = url.split("?schema=")[0]
        return url

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
