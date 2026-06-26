from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class RawFinancialStatement(Base):
    __tablename__ = "raw_financial_statements"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, ForeignKey("stocks.ticker"), nullable=False, index=True)
    provider = Column(String, nullable=False)
    statement_type = Column(String, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    period_end_date = Column(Date, nullable=False, index=True)
    raw_json = Column(JSONB, nullable=False)
    accession_number = Column(String)
    created_at = Column(DateTime, server_default=func.now())
