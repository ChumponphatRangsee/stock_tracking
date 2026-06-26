from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.data_ingestion_service import DataIngestionService
from app.services.stock_service import StockService

router = APIRouter()

async def run_sync_pipeline(ticker: str, db: Session):
    """Shorthand worker to run ingestion and recalculate scores sequentially."""
    try:
        ingestion_service = DataIngestionService(db)
        stock_service = StockService(db)
        
        # 1. Fetch raw data and write snapshots
        await ingestion_service.ingest_ticker(ticker)
        
        # 2. Recalculate and write scores
        stock_service.calculate_and_save_scores(ticker)
    except Exception as e:
        print(f"Sync pipeline failed for {ticker}: {e}")

@router.post("/{ticker}")
async def force_refresh_stock(
    ticker: str, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Manually triggers a full data fetch and score recalculation for a ticker.
    Runs asynchronously in a FastAPI background task to return a 202 Accepted instantly.
    """
    ticker_upper = ticker.upper()
    background_tasks.add_task(run_sync_pipeline, ticker_upper, db)
    return {"message": f"Refresh and recalculation pipeline triggered for {ticker_upper}. Processing in background..."}
