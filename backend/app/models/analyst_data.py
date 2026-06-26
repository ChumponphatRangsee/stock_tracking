from sqlalchemy import Column, String, Numeric, Integer, Date, DateTime, func, ForeignKey
from app.core.database import Base

class AnalystData(Base):
    __tablename__ = "analyst_data"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    snapshot_date = Column(Date, primary_key=True)
    
    target_price_avg = Column(Numeric)
    target_price_high = Column(Numeric)
    target_price_low = Column(Numeric)
    target_upside_pct = Column(Numeric)
    
    strong_buy = Column(Integer)
    buy = Column(Integer)
    hold = Column(Integer)
    sell = Column(Integer)
    strong_sell = Column(Integer)
    
    consensus_rating = Column(String)
    
    source = Column(String, default='Finnhub')
    created_at = Column(DateTime, server_default=func.now())