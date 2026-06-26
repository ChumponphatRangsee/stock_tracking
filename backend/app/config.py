from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = "http://localhost:8000"
    SUPABASE_KEY: str = "dummy_key"
    FMP_API_KEY: str = "dummy_fmp_key"
    FINNHUB_API_KEY: str = "dummy_finnhub_key"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()