from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class MarketDataProvider(ABC):
    """Interface for fetching basic company info and current quotes."""
    
    @abstractmethod
    async def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Returns standard profile: sector, industry, market cap."""
        pass
        
    @abstractmethod
    async def get_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Returns standard quote: price, volume, high_52w, low_52w."""
        pass