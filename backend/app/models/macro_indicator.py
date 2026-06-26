from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class MacroIndicator(Base):
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String, nullable=False, index=True)
    observation_date = Column(Date, nullable=False, index=True)
    value = Column(Numeric)
    source = Column(String, nullable=False)
    metadata_json = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())
