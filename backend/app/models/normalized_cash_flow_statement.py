from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func

from app.core.database import Base


class NormalizedCashFlowStatement(Base):
    __tablename__ = "normalized_cash_flow_statements"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    period_end_date = Column(Date, primary_key=True)
    period_type = Column(String, primary_key=True)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    operating_cash_flow = Column(Numeric)
    capital_expenditure = Column(Numeric)
    free_cash_flow = Column(Numeric)
    dividends_paid = Column(Numeric)
    share_buybacks = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
