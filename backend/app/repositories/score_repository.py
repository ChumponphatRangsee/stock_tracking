from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.stock_score import StockScore


class ScoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_snapshot(self, payload: dict) -> None:
        update_values = payload.copy()
        update_values.pop("ticker", None)
        update_values.pop("snapshot_date", None)
        update_values.pop("score_version", None)
        stmt = insert(StockScore).values(**payload).on_conflict_do_update(
            index_elements=["ticker", "snapshot_date", "score_version"],
            set_=update_values,
        )
        self.db.execute(stmt)

    def latest(self, ticker: str) -> Optional[StockScore]:
        return (
            self.db.query(StockScore)
            .filter(StockScore.ticker == ticker.upper())
            .order_by(StockScore.snapshot_date.desc())
            .first()
        )
