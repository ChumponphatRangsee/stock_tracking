from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, func
from app.core.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    ticker = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    sector = Column(String, index=True)
    industry = Column(String)
    exchange = Column(String)
    country = Column(String)
    market_cap = Column(BigInteger)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())