"""
Core configuration module for the AI Fitness Ecosystem backend.
Uses pydantic-settings for environment variable management following 12-Factor App methodology.
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "AI Fitness Ecosystem"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # ── Database ─────────────────────────────────────────────────
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "fitness_user"
    DB_PASSWORD: str = "fitness_pass_2024"
    DB_NAME: str = "ai_fitness_db"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ── JWT Authentication ───────────────────────────────────────
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production-2024"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── OTP ──────────────────────────────────────────────────────
    OTP_EXPIRE_MINUTES: int = 10
    OTP_LENGTH: int = 6

    # ── Google OAuth ─────────────────────────────────────────────
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/auth/google/callback"

    # ── OpenAI ───────────────────────────────────────────────────
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_VISION_MODEL: str = "gpt-4o"

    # ── Google Gemini ────────────────────────────────────────────
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # ── AI Provider ──────────────────────────────────────────────
    AI_PROVIDER: str = "openai"  # "openai" or "gemini"

    # ── Spotify ──────────────────────────────────────────────────
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None
    SPOTIFY_REDIRECT_URI: str = "http://localhost:3000/music/callback"

    # ── YouTube ──────────────────────────────────────────────────
    YOUTUBE_API_KEY: Optional[str] = None

    # ── Cloudinary ───────────────────────────────────────────────
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None

    # ── Power BI ─────────────────────────────────────────────────
    POWERBI_EMBED_URL: Optional[str] = None
    POWERBI_REPORT_ID: Optional[str] = None
    POWERBI_ACCESS_TOKEN: Optional[str] = None

    # ── Redis ────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Rate Limiting ────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

    # ── Email (OTP / Password Reset) ─────────────────────────────
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@aifitness.com"

    # ── File Upload ──────────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
