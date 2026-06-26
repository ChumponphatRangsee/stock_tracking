import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Monitor API"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "postgresql://postgres:password@localhost:5432/postgres")
    FMP_API_KEY: str = os.environ.get("FMP_API_KEY", "")
    FINNHUB_API_KEY: str = os.environ.get("FINNHUB_API_KEY", "")
    FRED_API_KEY: str = os.environ.get("FRED_API_KEY", "")
    SEC_USER_AGENT: str = os.environ.get("SEC_USER_AGENT", "stock-monitor/1.0 contact@example.com")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
