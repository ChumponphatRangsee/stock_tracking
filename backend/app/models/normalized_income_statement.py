from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func

from app.core.database import Base


class NormalizedIncomeStatement(Base):
    __tablename__ = "normalized_income_statements"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    period_end_date = Column(Date, primary_key=True)
    period_type = Column(String, primary_key=True)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    revenue = Column(Numeric)
    gross_profit = Column(Numeric)
    operating_income = Column(Numeric)
    ebit = Column(Numeric)
    net_income = Column(Numeric)
    eps_basic = Column(Numeric)
    eps_diluted = Column(Numeric)
    shares_basic = Column(Numeric)
    shares_diluted = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
