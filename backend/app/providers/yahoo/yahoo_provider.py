from datetime import date, datetime
from typing import Any, Dict, Optional

from app.providers.base.market_data_provider import MarketDataProvider
from app.providers.base.financial_data_provider import FinancialDataProvider
import yfinance as yf
import pandas as pd
import numpy as np


class YahooProvider(MarketDataProvider, FinancialDataProvider):
    """
    Yahoo Finance provider used as the primary v1 raw statement source.
    """

    def _to_native_float(self, val: Any) -> Optional[float]:
        if val is None or pd.isna(val):
            return None
        try:
            if isinstance(val, (np.floating, np.integer)):
                return float(val.item())
            return float(val)
        except Exception:
            return None

    def _sanitize(self, value: Any):
        if isinstance(value, dict):
            return {str(key): self._sanitize(val) for key, val in value.items()}
        if isinstance(value, list):
            return [self._sanitize(item) for item in value]
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, (np.integer, np.floating)):
            return float(value)
        if pd.isna(value):
            return None
        return value

    def _statement_rows(self, df: pd.DataFrame, ticker: str, statement_type: str, period_type: str) -> list[dict]:
        if df is None or df.empty:
            return []

        rows: list[dict] = []
        for column in df.columns:
            period_end = column.date() if hasattr(column, "date") else column
            line_items: dict[str, float] = {}
            for label in df.index:
                value = df.at[label, column]
                native_value = self._to_native_float(value)
                if native_value is not None:
                    line_items[str(label)] = native_value

            fiscal_quarter = ((period_end.month - 1) // 3) + 1 if period_type == "quarterly" else None
            rows.append(
                {
                    "ticker": ticker,
                    "provider": "Yahoo",
                    "statement_type": statement_type,
                    "fiscal_year": period_end.year,
                    "fiscal_quarter": fiscal_quarter,
                    "period_end_date": period_end,
                    "raw_json": {
                        "period_type": period_type,
                        "line_items": line_items,
                    },
                    "accession_number": None,
                }
            )

        rows.sort(key=lambda item: item["period_end_date"], reverse=True)
        return rows

    def _get_info(self, ticker: str) -> dict:
        return yf.Ticker(ticker).info

    async def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        try:
            info = self._get_info(ticker)
            
            return {
                "company_name": info.get("shortName") or info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "exchange": info.get("exchange"),
                "country": info.get("country"),
                "market_cap": info.get("marketCap")
            }
        except Exception as e:
            print(f"Error fetching profile from Yahoo for {ticker}: {e}")
            return None

    async def get_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        try:
            info = self._get_info(ticker)
            
            current_price = self._to_native_float(info.get("currentPrice") or info.get("regularMarketPrice"))
            high_52w = self._to_native_float(info.get("fiftyTwoWeekHigh"))
            low_52w = self._to_native_float(info.get("fiftyTwoWeekLow"))
            
            below_52w_pct = 0.0
            if high_52w and current_price and high_52w > current_price:
                below_52w_pct = ((high_52w - current_price) / high_52w) * 100

            return {
                "close_price": current_price,
                "volume": info.get("volume"),
                "high_52w": high_52w,
                "low_52w": low_52w,
                "below_52w_high_pct": round(below_52w_pct, 2) if below_52w_pct else 0.0
            }
        except Exception as e:
            print(f"Error fetching quote from Yahoo for {ticker}: {e}")
            return None

    async def get_financial_metrics(self, ticker: str) -> Optional[Dict[str, Any]]:
        try:
            info = self._get_info(ticker)
            return {
                "forward_pe": self._to_native_float(info.get("forwardPE")),
                "pe_ratio": self._to_native_float(info.get("trailingPE")),
                "ps_ratio": self._to_native_float(info.get("priceToSalesTrailing12Months")),
                "peg_ratio": self._to_native_float(info.get("pegRatio")),
                "eps_growth": self._to_native_float(info.get("earningsGrowth")),
                "target_price_avg": self._to_native_float(info.get("targetMeanPrice")),
                "target_price_high": self._to_native_float(info.get("targetHighPrice")),
                "target_price_low": self._to_native_float(info.get("targetLowPrice")),
            }
        except Exception as e:
            print(f"Error fetching metrics from Yahoo for {ticker}: {e}")
            return None

    async def get_raw_company_payload(self, ticker: str) -> dict:
        return self._sanitize(self._get_info(ticker))

    async def get_raw_financial_statements(self, ticker: str) -> list[Dict[str, Any]]:
        try:
            stock = yf.Ticker(ticker)
            return (
                self._statement_rows(stock.financials, ticker, "income_statement", "annual")
                + self._statement_rows(stock.quarterly_financials, ticker, "income_statement", "quarterly")
                + self._statement_rows(stock.balance_sheet, ticker, "balance_sheet", "annual")
                + self._statement_rows(stock.quarterly_balance_sheet, ticker, "balance_sheet", "quarterly")
                + self._statement_rows(stock.cashflow, ticker, "cash_flow_statement", "annual")
                + self._statement_rows(stock.quarterly_cashflow, ticker, "cash_flow_statement", "quarterly")
            )
        except Exception as e:
            print(f"Error fetching statements from Yahoo for {ticker}: {e}")
            return []
