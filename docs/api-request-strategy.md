# API Request Strategy & Provider Mapping

This document specifies which third-party data providers are mapped to each specific metric, preventing paid paywalls and avoiding API rate limits.

---

## 1. Data Mapping Matrix

| Capability Category | Target Metric | Primary Provider | Method |
| :--- | :--- | :--- | :--- |
| **Market Data** | Close Price | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Volume | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | 52-Week High | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | 52-Week Low | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Drawdown % | **Calculated** | Mathematical extraction in Yahoo Provider |
| **Company Profile** | Company Name | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Sector & Industry | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Exchange & Country | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Market Cap | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| **Financial Metrics** | Forward & Trailing PE| **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Price-to-Sales (PS) | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | PEG Ratio | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Return on Equity (ROE) | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Margins (Gross, Net, Op)| **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Debt-to-Equity (D/E) | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Current Ratio | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | EBIT Growth | **Yahoo Finance / Calculated**| Derived on-the-fly from raw financials |
| | ROIC | **Yahoo Finance / Calculated**| Derived on-the-fly from raw balance sheet |
| **Analyst Estimates** | Analyst Price Targets | **Yahoo Finance** | Native Scraper (`yf.Ticker(t).info`) |
| | Recommendation Trends| **Finnhub** | REST API (`/stock/recommendation`) |

---

## 2. API Quota Conservation Rules

1.  **Yahoo Finance (`yfinance`):** Has no hard daily call quotas. However, to prevent IP address rate blocks, we enforce a strict `asyncio.sleep(1.0)` delay inside our loops.
2.  **Finnhub:** Key is restricted to **60 requests per minute**.
    *   Our scheduler only calls Finnhub during the weekly weekend jobs to update recommendations.
    *   We bypass `/stock/price-target` on Finnhub entirely because they locked it on their free tier, saving API quota.
3.  **FMP (Financial Modeling Prep):** FMP is **completely disabled** as of Phase 3 because FMP blocks free tier accounts on all legacy profile, metric, and financials endpoints. Do not add FMP integrations without a premium billing upgrade.
