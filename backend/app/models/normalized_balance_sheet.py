from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func

from app.core.database import Base


class NormalizedBalanceSheet(Base):
    __tablename__ = "normalized_balance_sheets"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    period_end_date = Column(Date, primary_key=True)
    period_type = Column(String, primary_key=True)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    cash_and_equivalents = Column(Numeric)
    current_assets = Column(Numeric)
    total_assets = Column(Numeric)
    current_liabilities = Column(Numeric)
    total_liabilities = Column(Numeric)
    total_debt = Column(Numeric)
    total_equity = Column(Numeric)
    invested_capital = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
