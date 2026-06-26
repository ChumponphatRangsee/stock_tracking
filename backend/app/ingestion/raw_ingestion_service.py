from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.raw_data_repository import RawDataRepository


class RawIngestionService:
    def __init__(self, db: Session):
        self.repository = RawDataRepository(db)

    def store(self, provider: str, endpoint: str, ticker: str | None, data_type: str, payload: object) -> None:
        self.repository.save_response(
            provider=provider,
            endpoint=endpoint,
            ticker=ticker,
            data_type=data_type,
            payload=payload,
            fetched_at=datetime.utcnow(),
        )
