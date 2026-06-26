from sqlalchemy import Column, String, Numeric, BigInteger, Date, DateTime, func, ForeignKey
from app.core.database import Base

class StockPrice(Base):
    __tablename__ = "stock_prices"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    price_date = Column(Date, primary_key=True)
    close_price = Column(Numeric)
    open_price = Column(Numeric)
    high_price = Column(Numeric)
    low_price = Column(Numeric)
    volume = Column(BigInteger)
    high_52w = Column(Numeric)
    low_52w = Column(Numeric)
    below_52w_high_pct = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())