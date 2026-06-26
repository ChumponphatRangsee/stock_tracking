from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.stock_price import StockPrice
from app.repositories.valuation_repository import ValuationRepository


router = APIRouter()


@router.get("/{ticker}")
def get_latest_valuation(ticker: str, db: Session = Depends(get_db)):
    values = ValuationRepository(db).latest_by_ticker(ticker)
    if not values:
        raise HTTPException(status_code=404, detail=f"No valuation snapshot found for {ticker.upper()}")

    latest_price = (
        db.query(StockPrice)
        .filter(StockPrice.ticker == ticker.upper())
        .order_by(StockPrice.price_date.desc())
        .first()
    )
    current_price = float(getattr(latest_price, "close_price", 0.0) or 0.0)

    return {
        "ticker": ticker.upper(),
        "current_price": current_price,
        "valuations": [
            {
                "method": value.method,
                "valuation_date": value.valuation_date,
                "base_case_value": float(value.base_case_value or 0.0),
                "bear_case_value": float(value.bear_case_value or 0.0),
                "bull_case_value": float(value.bull_case_value or 0.0),
                "margin_of_safety_pct": float(value.margin_of_safety_pct or 0.0),
                "assumptions": value.assumptions_json,
            }
            for value in values
        ],
    }
