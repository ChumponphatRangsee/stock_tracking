from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class FinancialDataProvider(ABC):
    """Interface for fetching fundamental metrics and ratios."""
    
    @abstractmethod
    async def get_financial_metrics(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Returns standard metrics: PE, PS, ROE, margins, debt_equity."""
        pass