from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.stock_score import StockScore
from pydantic import BaseModel, ConfigDict

router = APIRouter()

# --- Pydantic Schemas ---
class ScoreSchema(BaseModel):
    ticker: str
    snapshot_date: date
    quality_score: float
    valuation_score: float
    discount_score: float
    analyst_score: float
    opportunity_score: float
    score_version: str

    model_config = ConfigDict(from_attributes=True)

# --- Routes ---

@router.get("/latest", response_model=List[ScoreSchema])
def get_latest_scores(db: Session = Depends(get_db)):
    """
    Retrieve the absolute latest scores for all active tickers.
    Uses PostgreSQL subquery to select only the newest snapshot_date for each ticker.
    """
    subquery = db.query(
        StockScore.ticker,
        StockScore.snapshot_date
    ).order_by(StockScore.ticker, StockScore.snapshot_date.desc()).distinct(StockScore.ticker).subquery()

    scores = db.query(StockScore).join(
        subquery,
        (StockScore.ticker == subquery.c.ticker) & 
        (StockScore.snapshot_date == subquery.c.snapshot_date)
    ).all()
    
    return scores

@router.get("/top", response_model=List[ScoreSchema])
def get_top_opportunities(limit: int = 20, db: Session = Depends(get_db)):
    """Retrieve the top opportunities ranked by their latest opportunity score."""
    subquery = db.query(
        StockScore.ticker,
        StockScore.snapshot_date
    ).order_by(StockScore.ticker, StockScore.snapshot_date.desc()).distinct(StockScore.ticker).subquery()

    scores = db.query(StockScore).join(
        subquery,
        (StockScore.ticker == subquery.c.ticker) & 
        (StockScore.snapshot_date == subquery.c.snapshot_date)
    ).order_by(StockScore.opportunity_score.desc()).limit(limit).all()
    
    return scores

@router.get("/{ticker}/history", response_model=List[ScoreSchema])
def get_score_history(ticker: str, db: Session = Depends(get_db)):
    """Retrieve the historical score trend for a specific stock (time-series)."""
    scores = db.query(StockScore).filter(
        StockScore.ticker == ticker.upper()
    ).order_by(StockScore.snapshot_date.asc()).all()
    
    return scores
