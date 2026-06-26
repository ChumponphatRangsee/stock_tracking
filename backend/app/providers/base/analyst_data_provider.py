from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AnalystDataProvider(ABC):
    """Interface for fetching analyst ratings and price targets."""
    
    @abstractmethod
    async def get_analyst_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Returns target prices and buy/hold/sell counts."""
        pass