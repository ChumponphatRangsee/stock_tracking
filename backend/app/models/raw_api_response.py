from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class RawApiResponse(Base):
    __tablename__ = "raw_api_responses"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    ticker = Column(String)
    data_type = Column(String, nullable=False, default="generic")
    raw_json = Column(JSONB)
    data_hash = Column(String)
    fetched_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
