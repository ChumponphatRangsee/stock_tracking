from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class IntrinsicValue(Base):
    __tablename__ = "intrinsic_values"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, ForeignKey("stocks.ticker"), nullable=False, index=True)
    valuation_date = Column(Date, nullable=False, index=True)
    method = Column(String, nullable=False)
    base_case_value = Column(Numeric)
    bear_case_value = Column(Numeric)
    bull_case_value = Column(Numeric)
    assumptions_json = Column(JSONB)
    margin_of_safety_pct = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
