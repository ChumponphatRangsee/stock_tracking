from app.providers.yahoo.yahoo_provider import YahooProvider
from app.providers.finnhub.finnhub_provider import FinnhubProvider
from sqlalchemy.orm import Session

class ProviderFactory:
    """
    Central hub to get the correct provider for a specific capability.
    This prevents business logic from depending on specific vendors.
    """
    
    @staticmethod
    def get_market_data_provider() -> YahooProvider:
        return YahooProvider()
        
    @staticmethod
    def get_financial_data_provider() -> YahooProvider:
        return YahooProvider()
        
    @staticmethod
    def get_analyst_data_provider(db: Session) -> FinnhubProvider:
        return FinnhubProvider(db)
