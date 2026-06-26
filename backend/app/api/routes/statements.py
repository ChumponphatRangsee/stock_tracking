from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.statement_repository import StatementRepository


router = APIRouter()


@router.get("/{ticker}")
def get_statements(
    ticker: str,
    period_type: str = "annual",
    limit: int = 4,
    db: Session = Depends(get_db),
):
    grouped = StatementRepository(db).list_grouped(ticker.upper(), period_type, limit)
    return {
        "ticker": ticker.upper(),
        "period_type": period_type,
        "statements": grouped,
    }
