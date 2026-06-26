import asyncio
from app.core.database import SessionLocal
from app.services.data_ingestion_service import DataIngestionService
from app.services.stock_service import StockService
from app.models.stock import Stock

def update_prices_and_scores_job():
    """
    Worker 1: Daily End-of-Day Price Update.
    Queries all active tickers from the database, fetches new prices,
    and recalculates their opportunity scores.
    """
    # 1. Create a fresh, isolated database session for this thread
    db = SessionLocal()
    try:
        # 2. Query all active stock tickers from the DB
        active_stocks = db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in active_stocks]
        
        if not tickers:
            print("[Scheduler] No active tickers found to update.")
            return

        print(f"[Scheduler] Daily Price & Score update started for {len(tickers)} stocks...")

        # 3. Initialize your services
        ingestion_service = DataIngestionService(db)
        stock_service = StockService(db)

        # 4. Define an internal async function to process all stocks sequentially
        async def process_all():
            for ticker in tickers:
                try:
                    # Fetch new price drawdown snapshots from Yahoo
                    await ingestion_service.ingest_ticker(ticker)
                    # Recalculate Quality, Valuation, Discount, Analyst, and Opportunity Scores
                    stock_service.calculate_and_save_scores(ticker)
                    # Basic courtesy delay to protect free API limits
                    await asyncio.sleep(1.0)
                except Exception as stock_err:
                    print(f"[Scheduler] Error processing ticker {ticker}: {stock_err}")

        # 5. Run the async task loop in this synchronous thread
        asyncio.run(process_all())
        print("[Scheduler] Daily Price & Score update completed.")

    except Exception as e:
        print(f"[Scheduler] Critical error in Daily Price Job: {e}")
    finally:
        # Always close the DB connection to prevent pool leakage!
        db.close()


def update_fundamentals_and_analysts_job():
    """
    Worker 2: Weekly Deep Fundamentals and Analyst Refresh.
    Updates company financial statements (EBIT, ROIC, PE) and Wall Street recommendations.
    """
    db = SessionLocal()
    try:
        active_stocks = db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in active_stocks]
        
        if not tickers:
            return

        print(f"[Scheduler] Weekly Fundamentals & Analyst update started for {len(tickers)} stocks...")
        ingestion_service = DataIngestionService(db)

        async def process_all():
            for ticker in tickers:
                try:
                    # In our V2 Ingestion Service, ingest_ticker naturally pulls everything
                    # including Yahoo Fundamentals and Finnhub recommendation counts!
                    await ingestion_service.ingest_ticker(ticker)
                    await asyncio.sleep(1.0)
                except Exception as stock_err:
                    print(f"[Scheduler] Error processing fundamental ticker {ticker}: {stock_err}")

        asyncio.run(process_all())
        print("[Scheduler] Weekly Fundamentals & Analyst update completed.")

    except Exception as e:
        print(f"[Scheduler] Critical error in Weekly Fundamentals Job: {e}")
    finally:
        db.close()
