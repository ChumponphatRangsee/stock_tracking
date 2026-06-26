from sqlalchemy import Column, String, Integer, Date, DateTime, func
from app.core.database import Base

class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"

    provider = Column(String, primary_key=True)
    usage_date = Column(Date, primary_key=True)
    request_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())