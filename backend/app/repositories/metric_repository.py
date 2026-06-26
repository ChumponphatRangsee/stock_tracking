from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.financial_metric import FinancialMetric


class MetricRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_snapshot(self, payload: dict) -> None:
        stmt = insert(FinancialMetric).values(**payload).on_conflict_do_nothing()
        self.db.execute(stmt)

    def latest(self, ticker: str) -> Optional[FinancialMetric]:
        return (
            self.db.query(FinancialMetric)
            .filter(FinancialMetric.ticker == ticker.upper())
            .order_by(FinancialMetric.snapshot_date.desc())
            .first()
        )
