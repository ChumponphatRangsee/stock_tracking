from sqlalchemy.orm import Session
from app.services.vi_pipeline_service import ViPipelineService

class DataIngestionService:
    """
    Compatibility wrapper over the newer VI pipeline service.
    """
    def __init__(self, db: Session):
        self.db = db
        self.pipeline_service = ViPipelineService(db)

    async def ingest_ticker(self, ticker: str):
        return await self.pipeline_service.refresh_raw(ticker)
