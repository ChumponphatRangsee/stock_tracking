import asyncio
from app.core.database import SessionLocal
from app.services.data_ingestion_service import DataIngestionService

async def test_ingestion():
    db = SessionLocal()
    try:
        service = DataIngestionService(db)
        # Test with Apple
        await service.ingest_ticker("AAPL")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_ingestion())