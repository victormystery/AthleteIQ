"""
Application settings and configuration
"""
import os
from functools import lru_cache
from typing import List, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _resolve_env_path() -> Optional[str]:
    env_file_override = os.getenv("ENV_FILE")
    environment = os.getenv("ENVIRONMENT", "development").lower()
    env_filename = ".env.prod" if environment in {"production", "prod"} else ".env"

    candidates = []
    if env_file_override:
        candidates.append(env_file_override)
    candidates.append(os.path.join(BASE_DIR, env_filename))
    candidates.append("/app/.env")
    candidates.append("/app/.env.prod")

    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def _load_environment() -> None:
    env_path = _resolve_env_path()
    if env_path:
        load_dotenv(env_path, override=False)


_load_environment()


class Settings(BaseSettings):
    """Application settings"""
    
    # App Information
    APP_NAME: str = "Sports Career Recommender API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Paths
    BASE_DIR: str = BASE_DIR
    MODEL_PATH: str = "sports_career_recommendation_model.pkl"
    TRAINING_DATA_PATH: str = os.path.join(BASE_DIR, "student-football-analysis", "data", "Student Sports Career Pathway Questionnaire (Responses) - Form Responses 1.csv")
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_PATH: Optional[str] = None
    GOOGLE_SHEETS_SPREADSHEET_ID: str = "1tT91nRZYuYtJ6EWUa51q1OuzyUPHpox4QVb8TMqa-r0"
    GOOGLE_SHEETS_WORKSHEET_NAME: str = "Form Responses 1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # Career Pathways Configuration
    TOTAL_RECOMMENDATIONS: int = 6
    ML_RECOMMENDATIONS: int = 5
    MOTIVATION_BASED_RECOMMENDATIONS: int = 1
    
    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Database
    DATABASE_URL: str = "sqlite:///./career_recommender.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Security - MUST be set in .env for production
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # JWT Security (alternative naming)
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env

    def get_secret_key(self) -> str:
        return self.SECRET_KEY

    def get_jwt_secret(self) -> str:
        return self.JWT_SECRET or self.SECRET_KEY

    def validate_secrets(self) -> None:
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing; set it in the backend .env")
        if not self.get_jwt_secret():
            raise ValueError("JWT secret is missing; set JWT_SECRET or SECRET_KEY in the backend .env")


class DevSettings(Settings):
    """Development settings"""

    ENVIRONMENT: str = "development"


class ProdSettings(Settings):
    """Production settings"""

    ENVIRONMENT: str = "production"


@lru_cache()
def get_settings() -> Settings:
    environment = os.getenv("ENVIRONMENT", "development").lower()
    if environment in {"production", "prod"}:
        return ProdSettings()
    return DevSettings()


settings = get_settings()
