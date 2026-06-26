__test__ = False

import asyncio
from app.core.database import SessionLocal
from app.services.stock_service import StockService

async def test_scoring():
    db = SessionLocal()
    try:
        service = StockService(db)
        # Calculate scores for Apple using the snapshots we just ingested!
        score = service.calculate_and_save_scores("AAPL")
        
        if score:
            print("\n--- RESULTS IN DATABASE ---")
            print(f"Ticker: {score.ticker}")
            print(f"Quality Score: {score.quality_score} / 100")
            print(f"Valuation Score: {score.valuation_score} / 100")
            print(f"Discount Score: {score.discount_score} / 100")
            print(f"Analyst Score: {score.analyst_score} / 100")
            print(f"OVERALL OPPORTUNITY SCORE: {score.opportunity_score} / 100")
            print("--------------------------\n")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_scoring())
