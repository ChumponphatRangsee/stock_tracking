from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.stock import Stock
from pydantic import BaseModel, ConfigDict

router = APIRouter()

# --- Pydantic Schemas ---
class StockSchema(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str]
    industry: Optional[str]
    exchange: Optional[str]
    country: Optional[str]
    market_cap: Optional[int]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# --- Routes ---

@router.get("/", response_model=List[StockSchema])
def get_stocks(sector: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve all monitored stocks, optionally filtered by sector."""
    query = db.query(Stock).filter(Stock.is_active == True)
    if sector:
        query = query.filter(Stock.sector == sector)
    return query.all()

@router.get("/{ticker}", response_model=StockSchema)
def get_stock(ticker: str, db: Session = Depends(get_db)):
    """Retrieve details for a specific stock."""
    stock = db.query(Stock).filter(Stock.ticker == ticker.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    return stock
