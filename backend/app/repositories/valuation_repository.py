from typing import Optional

from sqlalchemy.orm import Session

from app.models.intrinsic_value import IntrinsicValue


class ValuationRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_all(self, valuations: list[dict]) -> None:
        for valuation in valuations:
            self.db.add(IntrinsicValue(**valuation))

    def latest_by_ticker(self, ticker: str) -> list[IntrinsicValue]:
        latest_date = (
            self.db.query(IntrinsicValue.valuation_date)
            .filter(IntrinsicValue.ticker == ticker.upper())
            .order_by(IntrinsicValue.valuation_date.desc())
            .limit(1)
            .scalar()
        )
        if latest_date is None:
            return []
        return (
            self.db.query(IntrinsicValue)
            .filter(
                IntrinsicValue.ticker == ticker.upper(),
                IntrinsicValue.valuation_date == latest_date,
            )
            .all()
        )

    def latest_preferred(self, ticker: str) -> Optional[IntrinsicValue]:
        return (
            self.db.query(IntrinsicValue)
            .filter(IntrinsicValue.ticker == ticker.upper())
            .order_by(IntrinsicValue.valuation_date.desc(), IntrinsicValue.id.desc())
            .first()
        )
