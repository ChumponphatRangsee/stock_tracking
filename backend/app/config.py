from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str = "postgresql://postgres:password@localhost:5432/postgres"
    SUPABASE_KEY: str = "dummy_key"
    FMP_API_KEY: str = ""
    FINNHUB_API_KEY: str = ""
    FRED_API_KEY: str = ""
    SEC_USER_AGENT: str = "stock-monitor/1.0 contact@example.com"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
