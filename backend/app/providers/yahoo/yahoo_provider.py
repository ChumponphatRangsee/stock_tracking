from typing import Dict, Any, Optional
from app.providers.base.market_data_provider import MarketDataProvider
from app.providers.base.financial_data_provider import FinancialDataProvider
import yfinance as yf
import pandas as pd
import numpy as np

class YahooProvider(MarketDataProvider, FinancialDataProvider):
    """
    Yahoo Finance Provider implementing both Market Data and Financial Data interfaces.
    Now calculates EBIT Growth and ROIC on-the-fly and safely casts NumPy types to Python floats.
    """

    def _to_native_float(self, val: Any) -> Optional[float]:
        """Converts NumPy floats/ints to native Python floats to prevent DB engine crashes."""
        if val is None or pd.isna(val):
            return None
        try:
            # Check if it's a numpy scalar type
            if isinstance(val, (np.floating, np.integer)):
                return float(val.item())
            return float(val)
        except Exception:
            return None

    async def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
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
            stock = yf.Ticker(ticker)
            info = stock.info
            
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
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 1. Fetch basic info metrics and sanitize them immediately to native floats
            metrics = {
                "forward_pe": self._to_native_float(info.get("forwardPE")),
                "pe_ratio": self._to_native_float(info.get("trailingPE")),
                "ps_ratio": self._to_native_float(info.get("priceToSalesTrailing12Months")),
                "peg_ratio": self._to_native_float(info.get("pegRatio")),
                "revenue_growth": self._to_native_float(info.get("revenueGrowth")),
                "eps_growth": self._to_native_float(info.get("earningsGrowth")),
                "roe": self._to_native_float(info.get("returnOnEquity")),
                "ebit_margin": self._to_native_float(info.get("operatingMargins")), 
                "gross_margin": self._to_native_float(info.get("grossMargins")),
                "net_margin": self._to_native_float(info.get("profitMargins")),
                "debt_equity": self._to_native_float(info.get("debtToEquity")),
                "current_ratio": self._to_native_float(info.get("currentRatio")),
                "target_price_avg": self._to_native_float(info.get("targetMeanPrice")),
                "target_price_high": self._to_native_float(info.get("targetHighPrice")),
                "target_price_low": self._to_native_float(info.get("targetLowPrice")),
                "ebit_growth": None,
                "roic": None
            }

            # 2. Fetch raw Financial Statements to calculate EBIT Growth and ROIC
            financials = stock.financials
            balance_sheet = stock.balance_sheet

            if financials is not None and not financials.empty and balance_sheet is not None and not balance_sheet.empty:
                try:
                    # --- EBIT Growth Calculation ---
                    ebit_row = None
                    for label in ["EBIT", "Operating Income", "OperatingIncome"]:
                        if label in financials.index:
                            ebit_row = financials.loc[label]
                            break
                    
                    if ebit_row is not None and len(ebit_row) >= 2:
                        ebit_newest = ebit_row.iloc[0]
                        ebit_previous = ebit_row.iloc[1]
                        
                        if ebit_previous and ebit_previous != 0:
                            ebit_growth = ((ebit_newest - ebit_previous) / abs(ebit_previous))
                            metrics["ebit_growth"] = self._to_native_float(round(ebit_growth, 4))

                    # --- ROIC Calculation ---
                    if ebit_row is not None and len(ebit_row) > 0:
                        ebit = ebit_row.iloc[0]
                        
                        # Extract Balance Sheet metrics
                        total_debt = None
                        for label in ["Total Debt", "TotalDebt"]:
                            if label in balance_sheet.index:
                                total_debt = balance_sheet.loc[label].iloc[0]
                                break
                        if total_debt is None:
                            short_debt = balance_sheet.loc["Current Debt"] if "Current Debt" in balance_sheet.index else 0
                            long_debt = balance_sheet.loc["Long Term Debt"] if "Long Term Debt" in balance_sheet.index else 0
                            total_debt = float(short_debt.iloc[0] if hasattr(short_debt, 'iloc') else short_debt) + float(long_debt.iloc[0] if hasattr(long_debt, 'iloc') else long_debt)

                        total_equity = None
                        for label in ["Stockholders Equity", "Total Stockholders Equity", "TotalStockholdersEquity"]:
                            if label in balance_sheet.index:
                                total_equity = balance_sheet.loc[label].iloc[0]
                                break

                        cash = 0.0
                        for label in ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments", "CashAndCashEquivalents"]:
                            if label in balance_sheet.index:
                                cash = balance_sheet.loc[label].iloc[0]
                                break

                        if total_debt is not None and total_equity is not None:
                            invested_capital = total_debt + total_equity - cash
                            if invested_capital and invested_capital > 0:
                                roic = ebit / invested_capital
                                metrics["roic"] = self._to_native_float(round(roic, 4))

                except Exception as calc_error:
                    print(f"Calculations failed for {ticker}: {calc_error}")

            return metrics
            
        except Exception as e:
            print(f"Error fetching metrics from Yahoo for {ticker}: {e}")
            return None
