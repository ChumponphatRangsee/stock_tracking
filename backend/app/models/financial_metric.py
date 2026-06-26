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
    revenue_growth_1y = Column(Numeric)
    revenue_growth_3y_cagr = Column(Numeric)
    eps_growth = Column(Numeric)
    ebit_growth = Column(Numeric)
    ebit_growth_3y_cagr = Column(Numeric)
    fcf_growth_3y_cagr = Column(Numeric)
    
    roe = Column(Numeric)
    roic = Column(Numeric)
    roce = Column(Numeric)
    croic = Column(Numeric)
    ebit_margin = Column(Numeric)
    operating_margin = Column(Numeric)
    gross_margin = Column(Numeric)
    net_margin = Column(Numeric)
    fcf_margin = Column(Numeric)
    
    debt_equity = Column(Numeric)
    debt_to_equity = Column(Numeric)
    net_debt_to_ebit = Column(Numeric)
    current_ratio = Column(Numeric)
    fcf_yield = Column(Numeric)
    earnings_yield = Column(Numeric)
    ev_ebit = Column(Numeric)
    ev_fcf = Column(Numeric)
    buyback_yield = Column(Numeric)
    share_dilution_pct = Column(Numeric)
    
    source = Column(String, default='FMP')
    created_at = Column(DateTime, server_default=func.now())
