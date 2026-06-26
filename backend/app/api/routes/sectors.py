from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.models.stock import Stock
from app.models.stock_score import StockScore
from pydantic import BaseModel

router = APIRouter()

# --- Pydantic Schemas ---
class SectorScoreSchema(BaseModel):
    sector: str
    average_opportunity_score: float
    stock_count: int

# --- Routes ---

@router.get("/ranking", response_model=List[SectorScoreSchema])
def get_sector_rankings(db: Session = Depends(get_db)):
    """
    Ranks sectors by their average opportunity score.
    Uses the latest score snapshot for each stock, grouped by sector.
    """
    # 1. Subquery to find the latest score date for each ticker
    subquery = db.query(
        StockScore.ticker,
        StockScore.snapshot_date,
        StockScore.score_version,
    ).order_by(
        StockScore.ticker,
        StockScore.snapshot_date.desc(),
        StockScore.score_version.desc(),
    ).distinct(StockScore.ticker).subquery()

    # 2. Join Stock, StockScore, and the subquery to compute the aggregate averages
    rankings = db.query(
        Stock.sector,
        func.round(func.avg(StockScore.opportunity_score), 2).label("average_opportunity_score"),
        func.count(Stock.ticker).label("stock_count")
    ).join(
        StockScore, Stock.ticker == StockScore.ticker
    ).join(
        subquery,
        (StockScore.ticker == subquery.c.ticker) & 
        (StockScore.snapshot_date == subquery.c.snapshot_date) &
        (StockScore.score_version == subquery.c.score_version)
    ).filter(
        Stock.sector != None
    ).group_by(
        Stock.sector
    ).order_by(
        func.avg(StockScore.opportunity_score).desc()
    ).all()

    # Format result to match schema
    return [
        {
            "sector": row.sector,
            "average_opportunity_score": float(row.average_opportunity_score),
            "stock_count": int(row.stock_count)
        }
        for row in rankings
    ]
