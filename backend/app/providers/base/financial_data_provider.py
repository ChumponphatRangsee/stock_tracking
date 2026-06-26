from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class FinancialDataProvider(ABC):
    """Interface for fetching raw statement data and supplemental vendor metrics."""
    
    @abstractmethod
    async def get_financial_metrics(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Returns supplemental metrics such as vendor price multiples."""
        pass

    @abstractmethod
    async def get_raw_financial_statements(self, ticker: str) -> list[Dict[str, Any]]:
        """Returns raw statement snapshots suitable for normalization."""
        pass
