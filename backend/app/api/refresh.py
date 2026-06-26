from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.data_ingestion import ingest_stock_data

router = APIRouter()

@router.post("/{ticker}")
async def force_refresh_stock(ticker: str, background_tasks: BackgroundTasks):
    """
    Endpoint to manually trigger data ingestion for a specific stock.
    Runs as a background task to return a response immediately.
    """
    ticker = ticker.upper()
    background_tasks.add_task(ingest_stock_data, ticker)
    return {"message": f"Refresh triggered for {ticker}. Check database in a few moments."}
