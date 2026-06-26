import asyncio
from datetime import date
from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.models.stock_price import StockPrice
from app.models.financial_metric import FinancialMetric
from app.models.analyst_data import AnalystData
from app.providers.provider_factory import ProviderFactory
from sqlalchemy.dialects.postgresql import insert

class DataIngestionService:
    """
    Orchestrates the flow of data using the abstract Provider layer.
    """
    def __init__(self, db: Session):
        self.db = db
        # Get providers via the factory, not by hardcoding specific vendors
        self.market_provider = ProviderFactory.get_market_data_provider()
        self.financial_provider = ProviderFactory.get_financial_data_provider()
        self.analyst_provider = ProviderFactory.get_analyst_data_provider(db)

    async def ingest_ticker(self, ticker: str):
        """Fetches and saves all data points for a single ticker."""
        print(f"Starting ingestion for {ticker}...")
        today = date.today()

        # --- 1. Fetch Company Profile & Quote (Yahoo) ---
        profile_data = await self.market_provider.get_company_profile(ticker)
        quote_data = await self.market_provider.get_quote(ticker)
        
        current_price = 0.0
        
        if profile_data:
            # Upsert Stock Table
            stmt = insert(Stock).values(ticker=ticker, **profile_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['ticker'],
                set_=profile_data
            )
            self.db.execute(stmt)

        if quote_data:
            current_price = quote_data.get("close_price", 0.0)
            
            # Insert Price Snapshot
            price_stmt = insert(StockPrice).values(
                ticker=ticker,
                price_date=today,
                **quote_data
            ).on_conflict_do_nothing() 
            self.db.execute(price_stmt)

        # --- 2. Fetch Financial Metrics (Yahoo) ---
        metrics_data = await self.financial_provider.get_financial_metrics(ticker)
        
        # We split the metrics data into what belongs in FinancialMetric and what belongs in AnalystData
        target_keys = ["target_price_avg", "target_price_high", "target_price_low"]
        yahoo_analyst_data = {}
        
        if metrics_data:
            # Extract target fields for AnalystData
            for key in target_keys:
                if key in metrics_data:
                    yahoo_analyst_data[key] = metrics_data.pop(key)

            metric_stmt = insert(FinancialMetric).values(
                ticker=ticker,
                snapshot_date=today,
                source="Yahoo",
                **metrics_data
            ).on_conflict_do_nothing()
            self.db.execute(metric_stmt)

        # --- 3. Fetch Analyst Recommendations (Finnhub) ---
        finnhub_data = await self.analyst_provider.get_analyst_data(ticker)
        
        # We merge Finnhub's recommendation counts with Yahoo's price targets
        merged_analyst_data = {}
        if finnhub_data:
            merged_analyst_data.update(finnhub_data)
        if yahoo_analyst_data:
            merged_analyst_data.update(yahoo_analyst_data)

        if merged_analyst_data:
            # Calculate target upside percentage now that we know the current price and target price
            avg_target = merged_analyst_data.get("target_price_avg")
            if avg_target and current_price and current_price > 0:
                upside = ((avg_target - current_price) / current_price) * 100
                merged_analyst_data["target_upside_pct"] = round(upside, 2)
                
            analyst_stmt = insert(AnalystData).values(
                ticker=ticker,
                snapshot_date=today,
                source="Finnhub/Yahoo",
                **merged_analyst_data
            ).on_conflict_do_nothing()
            self.db.execute(analyst_stmt)

        self.db.commit()
        print(f"Finished ingestion for {ticker}.")
