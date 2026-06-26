from sqlalchemy import Column, String, Numeric, Date, DateTime, func, ForeignKey
from app.core.database import Base

class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    ticker = Column(String, ForeignKey("stocks.ticker"), primary_key=True)
    snapshot_date = Column(Date, primary_key=True)
    
    forward_pe = Column(Numeric)
    pe_ratio = Column(Numeric)
    ps_ratio = Column(Numeric)
    peg_ratio = Column(Numeric)
    
    revenue_growth = Column(Numeric)
    eps_growth = Column(Numeric)
    ebit_growth = Column(Numeric)
    
    roe = Column(Numeric)
    roic = Column(Numeric)
    ebit_margin = Column(Numeric)
    gross_margin = Column(Numeric)
    net_margin = Column(Numeric)
    
    debt_equity = Column(Numeric)
    current_ratio = Column(Numeric)
    
    source = Column(String, default='FMP')
    created_at = Column(DateTime, server_default=func.now())