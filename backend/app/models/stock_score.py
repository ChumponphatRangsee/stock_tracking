from sqlalchemy import Column, String, Numeric, Date, DateTime, func, ForeignKey
from app.core.database import Base

class StockScore(Base):
    __tablename__ = "stock_scores"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    snapshot_date = Column(Date, primary_key=True)
    score_version = Column(String, default='v1', primary_key=True)
    
    quality_score = Column(Numeric)
    valuation_score = Column(Numeric)
    discount_score = Column(Numeric)
    analyst_score = Column(Numeric)
    trend_score = Column(Numeric)
    risk_score = Column(Numeric)
    margin_of_safety_score = Column(Numeric)
    opportunity_score = Column(Numeric, index=True)
    
    created_at = Column(DateTime, server_default=func.now())
