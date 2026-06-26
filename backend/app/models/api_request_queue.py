from sqlalchemy import Column, String, Integer, DateTime, Text, func
from app.core.database import Base

class ApiRequestQueue(Base):
    __tablename__ = "api_request_queue"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    ticker = Column(String)
    priority = Column(Integer, default=100)
    
    status = Column(String, default='PENDING', index=True)
    retry_count = Column(Integer, default=0)
    execute_after = Column(DateTime, server_default=func.now())
    
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())