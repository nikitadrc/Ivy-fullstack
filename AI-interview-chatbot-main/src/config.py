from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ivy - Interview Virtual Assistant"
    
    # Security
    SECRET_KEY: str = "bc12adbd5e7f4a69b24cc9b2009907cc39e939f5937a8f8fe3aa04462581692c"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:oEImqAplMmGEiprMmHuwAdqhzjZCWmxD@postgres.railway.internal:5432/railway"
    
    # Redis
    REDIS_URL: str = "redis://default:ajPCdzj5AWIvofYq4X7ULLIHFzB3xVIZ@redis-15910.c11.us-east-1-2.ec2.redns.redis-cloud.com:15910"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        os.getenv("FRONTEND_URL", ""),
    ]
    
    # OAuth2 settings
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    
    # JWT
    JWT_SECRET_KEY: str = "bc12adbd5e7f4a69b24cc9b2009907cc39e939f5937a8f8fe3aa04462581692c"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 60 * 24  # 24 hours
    
    # File Storage
    UPLOAD_FOLDER: str = "uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}
    
    # Analytics
    ANALYTICS_RETENTION_DAYS: int = 90
    
    # WebSocket
    WS_MESSAGE_QUEUE: str = "ws_messages"
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        case_sensitive = True

settings = Settings() 