from typing import Optional

from sqlalchemy.orm import Session

from app.clients.api_manager import ApiManager
from app.core.config import settings


class FredProvider:
    def __init__(self, db: Session):
        self.api_manager = ApiManager(db)
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.series = {
            "treasury_yield": "DGS10",
            "federal_funds_rate": "FEDFUNDS",
            "cpi_inflation": "CPIAUCSL",
            "unemployment_rate": "UNRATE",
        }

    async def get_series(self, indicator_name: str) -> list[dict]:
        api_key = settings.FRED_API_KEY
        if not api_key:
            return []
        series_id = self.series[indicator_name]
        payload = await self.api_manager.execute_request(
            "FRED",
            None,
            self.base_url,
            data_type=indicator_name,
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
            },
        )
        return (payload or {}).get("observations", [])

    async def fetch_all(self) -> dict[str, list[dict]]:
        results: dict[str, list[dict]] = {}
        for indicator_name in self.series:
            results[indicator_name] = await self.get_series(indicator_name)
        return results
