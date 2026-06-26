from sqlalchemy.orm import Session

class ProviderFactory:
    """
    Central hub to get the correct provider for a specific capability.
    This prevents business logic from depending on specific vendors.
    """
    
    @staticmethod
    def get_market_data_provider():
        from app.providers.yahoo.yahoo_provider import YahooProvider
        return YahooProvider()
        
    @staticmethod
    def get_financial_data_provider():
        from app.providers.yahoo.yahoo_provider import YahooProvider
        return YahooProvider()
        
    @staticmethod
    def get_analyst_data_provider(db: Session):
        from app.providers.finnhub.finnhub_provider import FinnhubProvider
        return FinnhubProvider(db)

    @staticmethod
    def get_sec_provider(db: Session):
        from app.providers.sec_edgar.sec_edgar_provider import SecEdgarProvider
        return SecEdgarProvider(db)

    @staticmethod
    def get_fred_provider(db: Session):
        from app.providers.fred.fred_provider import FredProvider
        return FredProvider(db)
