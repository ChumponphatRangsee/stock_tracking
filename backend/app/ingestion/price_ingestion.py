from datetime import date

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.stock_price import StockPrice


class PriceIngestion:
    def __init__(self, db: Session):
        self.db = db

    def store_snapshot(self, ticker: str, quote_data: dict) -> None:
        stmt = insert(StockPrice).values(
            ticker=ticker,
            price_date=date.today(),
            **quote_data,
        ).on_conflict_do_nothing()
        self.db.execute(stmt)
