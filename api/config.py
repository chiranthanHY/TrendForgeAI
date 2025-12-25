import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://neondb_owner:npg_KxLenyHP6vw8@ep-blue-star-ahf4guxx-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "TrendForgeAI"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://trendforge-dashboard.vercel.app"
    ]
    
    # Gemini API
    GEMINI_API_KEY: str = ""
    
    # Slack Integration
    SLACK_WEBHOOK_URL: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    # Try to load secrets from credentials.py if available and not set in env
    try:
        import credentials
        if not s.GEMINI_API_KEY and hasattr(credentials, 'GEMINI_API_KEY'):
            s.GEMINI_API_KEY = credentials.GEMINI_API_KEY
        if not s.SLACK_WEBHOOK_URL and hasattr(credentials, 'SLACK_WEBHOOK_URL'):
            s.SLACK_WEBHOOK_URL = credentials.SLACK_WEBHOOK_URL
    except ImportError:
        pass
    return s

settings = get_settings()
