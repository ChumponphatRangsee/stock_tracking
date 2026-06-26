# Database Schema & Snapshot Strategy Documentation

This document outlines the database architecture, table definitions, relationships, and indexing designed specifically for the **Historical Snapshot Schema**.

---

## 1. ER Diagram Summary

All key tables are designed for time-series snapshot storage using composite primary keys combining `ticker` and a date field (`snapshot_date` or `price_date`). 

```text
  [stocks] (1) 
     │
     ├───> [stock_prices]       (M) (PK: ticker, price_date)
     ├───> [financial_metrics]  (M) (PK: ticker, snapshot_date)
     ├───> [analyst_data]       (M) (PK: ticker, snapshot_date)
     ├───> [stock_scores]       (M) (PK: ticker, snapshot_date, score_version)
     └───> [watchlists]         (M) (PK: id, FK: ticker)
```

---

## 2. Table Definitions (SQL)

The following tables have been initialized in Supabase PostgreSQL:

```sql
-- 1. Stocks Table (The Core Registry)
CREATE TABLE stocks (
    ticker VARCHAR PRIMARY KEY,
    company_name VARCHAR NOT NULL,
    sector VARCHAR,
    industry VARCHAR,
    exchange VARCHAR,
    country VARCHAR,
    market_cap BIGINT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. Stock Prices (Daily Market Quotes)
CREATE TABLE stock_prices (
    ticker VARCHAR REFERENCES stocks(ticker),
    price_date DATE NOT NULL,
    close_price NUMERIC,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    volume BIGINT,
    high_52w NUMERIC,
    low_52w NUMERIC,
    below_52w_high_pct NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (ticker, price_date)
);

-- 3. Financial Metrics (Fundamental Balance Sheet & Margins Snapshot)
CREATE TABLE financial_metrics (
    ticker VARCHAR REFERENCES stocks(ticker),
    snapshot_date DATE NOT NULL,
    forward_pe NUMERIC,
    pe_ratio NUMERIC,
    ps_ratio NUMERIC,
    peg_ratio NUMERIC,
    revenue_growth NUMERIC,
    eps_growth NUMERIC,
    ebit_growth NUMERIC,
    roe NUMERIC,
    roic NUMERIC,
    ebit_margin NUMERIC,
    gross_margin NUMERIC,
    net_margin NUMERIC,
    debt_equity NUMERIC,
    current_ratio NUMERIC,
    source VARCHAR DEFAULT 'Yahoo',
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (ticker, snapshot_date)
);

-- 4. Analyst Data (Wall Street targets and Consensus)
CREATE TABLE analyst_data (
    ticker VARCHAR REFERENCES stocks(ticker),
    snapshot_date DATE NOT NULL,
    target_price_avg NUMERIC,
    target_price_high NUMERIC,
    target_price_low NUMERIC,
    target_upside_pct NUMERIC,
    strong_buy INT DEFAULT 0,
    buy INT DEFAULT 0,
    hold INT DEFAULT 0,
    sell INT DEFAULT 0,
    strong_sell INT DEFAULT 0,
    consensus_rating VARCHAR,
    source VARCHAR DEFAULT 'Finnhub/Yahoo',
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (ticker, snapshot_date)
);

-- 5. Stock Scores (The calculated Opportunity Rankings)
CREATE TABLE stock_scores (
    ticker VARCHAR REFERENCES stocks(ticker),
    snapshot_date DATE NOT NULL,
    score_version VARCHAR DEFAULT 'v1',
    quality_score NUMERIC,
    valuation_score NUMERIC,
    discount_score NUMERIC,
    analyst_score NUMERIC,
    opportunity_score NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (ticker, snapshot_date, score_version)
);

-- 6. Watchlists
CREATE TABLE watchlists (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR REFERENCES stocks(ticker),
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 7. API Request Queue (APScheduler task management)
CREATE TABLE api_request_queue (
    id SERIAL PRIMARY KEY,
    provider VARCHAR NOT NULL,
    endpoint VARCHAR NOT NULL,
    ticker VARCHAR,
    priority INT DEFAULT 100,
    status VARCHAR DEFAULT 'PENDING',
    retry_count INT DEFAULT 0,
    execute_after TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 8. API Usage Logs (Quota Enforcement)
CREATE TABLE api_usage_logs (
    provider VARCHAR NOT NULL,
    usage_date DATE NOT NULL,
    request_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (provider, usage_date)
);

-- 9. Raw API Responses (Cache check and Delta Delta audits)
CREATE TABLE raw_api_responses (
    id SERIAL PRIMARY KEY,
    provider VARCHAR NOT NULL,
    endpoint VARCHAR NOT NULL,
    ticker VARCHAR,
    response_hash VARCHAR,
    response_json JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 3. Database Indexes

These indexes have been optimized to allow lightning-fast queries when filtering the Screener on the React UI, or joining historical scores for charts:

```sql
CREATE INDEX idx_stock_prices_ticker_date ON stock_prices(ticker, price_date DESC);
CREATE INDEX idx_financial_metrics_ticker_date ON financial_metrics(ticker, snapshot_date DESC);
CREATE INDEX idx_analyst_data_ticker_date ON analyst_data(ticker, snapshot_date DESC);
CREATE INDEX idx_stock_scores_ticker_date ON stock_scores(ticker, snapshot_date DESC);
CREATE INDEX idx_stock_scores_opportunity ON stock_scores(opportunity_score DESC);
CREATE INDEX idx_api_request_queue_status_priority ON api_request_queue(status, priority, execute_after);
CREATE INDEX idx_stocks_sector ON stocks(sector);
```
