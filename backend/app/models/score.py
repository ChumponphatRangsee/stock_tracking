from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScoreBase(BaseModel):
    ticker: str
    quality_score: Optional[float] = None
    valuation_score: Optional[float] = None
    discount_score: Optional[float] = None
    analyst_score: Optional[float] = None
    opportunity_score: Optional[float] = None

class ScoreResponse(ScoreBase):
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
