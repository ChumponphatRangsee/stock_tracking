import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Monitor API"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "postgresql://postgres:password@localhost:5432/postgres")
    FMP_API_KEY: str = os.environ.get("FMP_API_KEY", "")
    FINNHUB_API_KEY: str = os.environ.get("FINNHUB_API_KEY", "")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()