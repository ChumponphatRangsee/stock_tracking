from typing import Dict, Any, Optional
from app.providers.base.analyst_data_provider import AnalystDataProvider
from app.core.config import settings
from app.clients.api_manager import ApiManager
from sqlalchemy.orm import Session

class FinnhubProvider(AnalystDataProvider):
    """
    Finnhub Provider implementing the Analyst Data interface.
    Now strictly queries recommendations since targets are restricted on free tier.
    """
    
    def __init__(self, db: Session):
        self.api_manager = ApiManager(db)
        self.provider = "Finnhub"
        self.base_url = "https://finnhub.io/api/v1"

    async def get_analyst_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetches recommendations from Finnhub."""
        
        recs_url = f"{self.base_url}/stock/recommendation?symbol={ticker}&token={settings.FINNHUB_API_KEY}"
        
        try:
            raw_recs = await self.api_manager.execute_request(
                self.provider,
                ticker,
                recs_url,
                data_type="analyst_recommendations",
            )
            
            normalized = {
                "strong_buy": 0, "buy": 0, "hold": 0, "sell": 0, "strong_sell": 0
            }

            if raw_recs and len(raw_recs) > 0:
                latest = raw_recs[0]
                normalized.update({
                    "strong_buy": latest.get("strongBuy", 0),
                    "buy": latest.get("buy", 0),
                    "hold": latest.get("hold", 0),
                    "sell": latest.get("sell", 0),
                    "strong_sell": latest.get("strongSell", 0)
                })
                
            return normalized
            
        except Exception as e:
            print(f"Error fetching analyst data from Finnhub for {ticker}: {e}")
            return None
