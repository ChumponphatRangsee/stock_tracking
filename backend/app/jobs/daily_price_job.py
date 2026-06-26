import asyncio

from app.core.database import SessionLocal
from app.repositories.stock_repository import StockRepository
from app.services.stock_service import StockService
from app.services.vi_pipeline_service import ViPipelineService


def run_daily_price_job():
    db = SessionLocal()
    try:
        tickers = StockRepository(db).get_active_tickers()
        if not tickers:
            return

        async def process_all():
            for ticker in tickers:
                try:
                    await ViPipelineService(db).refresh_raw(ticker)
                    StockService(db).calculate_and_save_scores(ticker)
                    await asyncio.sleep(0.5)
                except Exception as exc:
                    print(f"[Scheduler] Daily price job failed for {ticker}: {exc}")

        asyncio.run(process_all())
    finally:
        db.close()
