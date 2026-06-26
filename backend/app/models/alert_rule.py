from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, func, ForeignKey
from app.core.database import Base

class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, ForeignKey("stocks.ticker"), nullable=False)
    metric = Column(String, nullable=False)  # e.g., 'price', 'pe_ratio', 'margin_of_safety'
    condition = Column(String, nullable=False)  # e.g., 'less_than', 'greater_than'
    value_threshold = Column(Numeric, nullable=False)
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
