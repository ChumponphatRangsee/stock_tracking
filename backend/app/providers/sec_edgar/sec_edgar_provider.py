import asyncio
from typing import Optional

from sqlalchemy.orm import Session

from app.clients.api_manager import ApiManager
from app.core.config import settings


class SecEdgarProvider:
    def __init__(self, db: Session):
        self.api_manager = ApiManager(db)
        self.base_url = "https://data.sec.gov"
        self.headers = {"User-Agent": settings.SEC_USER_AGENT}

    async def _throttle(self) -> None:
        await asyncio.sleep(0.2)

    async def get_ticker_mapping(self) -> dict:
        await self._throttle()
        return await self.api_manager.execute_request(
            "SEC",
            None,
            "https://www.sec.gov/files/company_tickers.json",
            data_type="ticker_mapping",
            headers=self.headers,
        ) or {}

    async def get_cik_for_ticker(self, ticker: str) -> Optional[str]:
        mapping = await self.get_ticker_mapping()
        target = ticker.upper()
        for _, entry in mapping.items():
            if entry.get("ticker") == target:
                return str(entry.get("cik_str", "")).zfill(10)
        return None

    async def get_company_facts(self, ticker: str) -> Optional[dict]:
        cik = await self.get_cik_for_ticker(ticker)
        if not cik:
            return None
        await self._throttle()
        return await self.api_manager.execute_request(
            "SEC",
            ticker,
            f"{self.base_url}/api/xbrl/companyfacts/CIK{cik}.json",
            data_type="company_facts",
            headers=self.headers,
        )

    async def get_income_statement_facts(self, ticker: str) -> Optional[dict]:
        return await self.get_company_facts(ticker)

    async def get_balance_sheet_facts(self, ticker: str) -> Optional[dict]:
        return await self.get_company_facts(ticker)

    async def get_cash_flow_facts(self, ticker: str) -> Optional[dict]:
        return await self.get_company_facts(ticker)
