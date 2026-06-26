from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.clients.api_manager import ApiManager


class RawDataRepository:
    def __init__(self, db: Session):
        self.db = db
        self.api_manager = ApiManager(db)

    def save_response(
        self,
        provider: str,
        endpoint: str,
        ticker: Optional[str],
        data_type: str,
        payload: object,
        fetched_at: Optional[datetime] = None,
    ) -> None:
        self.api_manager.save_raw_response(
            provider=provider,
            ticker=ticker,
            endpoint=endpoint,
            data=payload,
            data_type=data_type,
            fetched_at=fetched_at,
        )
