from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.watchlist import Watchlist
from app.models.stock import Stock
from pydantic import BaseModel, ConfigDict

router = APIRouter()

# --- Pydantic Schemas ---
class WatchlistCreate(BaseModel):
    ticker: str
    note: Optional[str] = None

class WatchlistResponse(BaseModel):
    id: int
    ticker: str
    note: Optional[str]
    created_at: datetime
    
    # We join company name for a better frontend experience
    company_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- Routes ---

@router.get("/", response_model=List[WatchlistResponse])
def get_watchlist(db: Session = Depends(get_db)):
    """Retrieve all watchlisted items joined with their company names."""
    items = db.query(
        Watchlist.id,
        Watchlist.ticker,
        Watchlist.note,
        Watchlist.created_at,
        Stock.company_name
    ).outerjoin(
        Stock, Watchlist.ticker == Stock.ticker
    ).order_by(Watchlist.created_at.desc()).all()

    return [
        WatchlistResponse(
            id=item.id,
            ticker=item.ticker,
            note=item.note,
            created_at=item.created_at,
            company_name=item.company_name
        )
        for item in items
    ]

@router.post("/", response_model=WatchlistResponse)
def add_to_watchlist(item: WatchlistCreate, db: Session = Depends(get_db)):
    """Adds a stock ticker to the user's watchlist."""
    ticker_upper = item.ticker.upper()
    
    # Check if stock is registered in the universe
    stock_exists = db.query(Stock).filter(Stock.ticker == ticker_upper).first()
    if not stock_exists:
        raise HTTPException(
            status_code=400, 
            detail=f"Ticker {ticker_upper} must exist in the stocks universe before adding to watchlist"
        )

    # Check if already watchlisted
    already_watchlisted = db.query(Watchlist).filter(Watchlist.ticker == ticker_upper).first()
    if already_watchlisted:
        raise HTTPException(status_code=400, detail=f"Ticker {ticker_upper} is already watchlisted")

    watchlist_item = Watchlist(
        ticker=ticker_upper,
        note=item.note
    )
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    
    # Attach company name for the schema response
    watchlist_item.company_name = stock_exists.company_name
    return watchlist_item

@router.delete("/{ticker}")
def remove_from_watchlist(ticker: str, db: Session = Depends(get_db)):
    """Removes a stock ticker from the watchlist."""
    watchlist_item = db.query(Watchlist).filter(Watchlist.ticker == ticker.upper()).first()
    if not watchlist_item:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found in watchlist")
        
    db.delete(watchlist_item)
    db.commit()
    return {"message": f"Successfully removed {ticker.upper()} from watchlist"}
