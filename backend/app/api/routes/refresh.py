from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.vi_pipeline_service import ViPipelineService

router = APIRouter()

@router.post("/{ticker}/raw")
async def refresh_raw_stock(ticker: str, db: Session = Depends(get_db)):
    return await ViPipelineService(db).refresh_raw(ticker)


@router.post("/{ticker}/full-vi")
async def refresh_full_vi_stock(ticker: str, db: Session = Depends(get_db)):
    return await ViPipelineService(db).refresh_full_vi(ticker)


@router.post("/{ticker}")
async def force_refresh_stock(ticker: str, db: Session = Depends(get_db)):
    return await ViPipelineService(db).refresh_full_vi(ticker)
