from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class RawApiResponse(Base):
    __tablename__ = "raw_api_responses"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    ticker = Column(String)
    
    response_hash = Column(String)
    response_json = Column(JSONB)
    
    created_at = Column(DateTime, server_default=func.now())