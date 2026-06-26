from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.metric_repository import MetricRepository


router = APIRouter()


class MetricSchema(BaseModel):
    ticker: str
    snapshot_date: date
    revenue_growth_1y: float | None = None
    revenue_growth_3y_cagr: float | None = None
    ebit_growth_3y_cagr: float | None = None
    fcf_growth_3y_cagr: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    fcf_margin: float | None = None
    roe: float | None = None
    roic: float | None = None
    roce: float | None = None
    croic: float | None = None
    debt_to_equity: float | None = None
    net_debt_to_ebit: float | None = None
    current_ratio: float | None = None
    fcf_yield: float | None = None
    earnings_yield: float | None = None
    ev_ebit: float | None = None
    ev_fcf: float | None = None
    buyback_yield: float | None = None
    share_dilution_pct: float | None = None

    model_config = ConfigDict(from_attributes=True)


@router.get("/{ticker}", response_model=MetricSchema)
def get_latest_metrics(ticker: str, db: Session = Depends(get_db)):
    metric = MetricRepository(db).latest(ticker)
    if not metric:
        raise HTTPException(status_code=404, detail=f"No metric snapshot found for {ticker.upper()}")
    return metric
