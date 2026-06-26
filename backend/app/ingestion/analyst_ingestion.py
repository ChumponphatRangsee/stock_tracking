from datetime import date

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.analyst_data import AnalystData


class AnalystIngestion:
    def __init__(self, db: Session):
        self.db = db

    def store_snapshot(self, ticker: str, analyst_data: dict) -> None:
        payload = dict(analyst_data)
        stmt = insert(AnalystData).values(
            ticker=ticker,
            snapshot_date=date.today(),
            source=payload.pop("source", "Finnhub/Yahoo"),
            **payload,
        ).on_conflict_do_nothing()
        self.db.execute(stmt)
