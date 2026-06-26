from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.stock import Stock


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, ticker: str, profile_data: dict) -> None:
        payload = {"ticker": ticker, **profile_data}
        stmt = insert(Stock).values(**payload)
        stmt = stmt.on_conflict_do_update(index_elements=["ticker"], set_=profile_data)
        self.db.execute(stmt)

    def get_active_tickers(self) -> list[str]:
        return [
            stock.ticker
            for stock in self.db.query(Stock).filter(Stock.is_active.is_(True)).all()
        ]

    def get(self, ticker: str) -> Optional[Stock]:
        return self.db.query(Stock).filter(Stock.ticker == ticker.upper()).first()
