from sqlalchemy import Column, String, Integer, Text, DateTime, func, ForeignKey
from app.core.database import Base

class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, ForeignKey("stocks.ticker"))
    note = Column(Text)
    created_at = Column(DateTime, server_default=func.now())