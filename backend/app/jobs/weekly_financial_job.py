import asyncio

from app.core.database import SessionLocal
from app.repositories.stock_repository import StockRepository
from app.services.vi_pipeline_service import ViPipelineService


def run_weekly_financial_job():
    db = SessionLocal()
    try:
        tickers = StockRepository(db).get_active_tickers()
        if not tickers:
            return

        async def process_all():
            for ticker in tickers:
                try:
                    await ViPipelineService(db).refresh_full_vi(ticker)
                    await asyncio.sleep(0.5)
                except Exception as exc:
                    print(f"[Scheduler] Weekly VI job failed for {ticker}: {exc}")

        asyncio.run(process_all())
    finally:
        db.close()
