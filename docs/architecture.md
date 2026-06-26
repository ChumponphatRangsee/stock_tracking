# System Architecture Documentation

This document describes the current backend architecture after the raw-data-first value-investing refactor.

## 1. High-Level Flow

```text
       [React Frontend]
              |
              v
       [FastAPI Routes]
              |
              v
     [VI Pipeline Service]
              |
              +--> [Providers]
              |       - Yahoo
              |       - Finnhub
              |       - SEC EDGAR
              |       - FRED
              |
              +--> [Raw Storage]
              |       - raw_api_responses
              |       - raw_financial_statements
              |
              +--> [Normalization]
              |       - normalized_income_statements
              |       - normalized_balance_sheets
              |       - normalized_cash_flow_statements
              |
              +--> [Metrics Engine]
              |
              +--> [Valuation Engine]
              |
              +--> [Scoring Engine]
              |
              v
       [PostgreSQL Snapshots]
```

## 2. Main Backend Layers

### A. Routes
`backend/app/api/routes/`

Responsibilities:
- expose HTTP endpoints
- validate inputs
- return stable response contracts

Important routes:
- `/api/scores/latest`
- `/api/scores/top`
- `/api/metrics/{ticker}`
- `/api/valuation/{ticker}`
- `/api/statements/{ticker}`
- `/api/refresh/{ticker}/raw`
- `/api/refresh/{ticker}/full-vi`

### B. Services
`backend/app/services/`

Primary orchestrators:
- `ViPipelineService`: main raw-data-first staged pipeline
- `StockService`: score calculation from persisted snapshots
- `DataIngestionService`: compatibility wrapper over the pipeline
- `QuotaService`: provider quota accounting

Pipeline stages:
1. fetch market/profile/supplemental payloads
2. fetch raw financial statements
3. fetch analyst data
4. fetch SEC enrichment
5. fetch macro data
6. normalize statements
7. calculate metrics
8. calculate intrinsic values
9. calculate scores

The pipeline is designed for partial success. One provider failure should not crash the whole ticker refresh.

### C. Providers
`backend/app/providers/`

Provider roles:
- Yahoo: primary v1 quote/profile/statement source
- Finnhub: analyst recommendation source
- SEC EDGAR: company facts skeleton and enrichment path
- FRED: macro indicator skeleton

`ProviderFactory` resolves provider instances and keeps orchestration code decoupled from concrete adapters.

### D. Ingestion and Normalization
`backend/app/ingestion/`
`backend/app/normalization/`

Responsibilities:
- persist raw payloads
- persist raw statements
- normalize provider-specific statement shapes into internal models

Normalization is the boundary between vendor-specific data and internal business logic.

### E. Metrics, Valuation, and Scoring
`backend/app/metrics/`
`backend/app/valuation/`
`backend/app/scoring/`

These layers should remain side-effect free.

Responsibilities:
- `metrics/`: profitability, growth, balance sheet, cash flow, capital allocation, valuation metrics
- `valuation/`: DCF, owner earnings, margin of safety, placeholders for reverse DCF and EPV
- `scoring/`: quality, valuation, trend, risk, analyst, opportunity, and legacy discount scoring

### F. Repositories and Models
`backend/app/repositories/`
`backend/app/models/`

Responsibilities:
- append-only writes
- latest snapshot reads
- table-level persistence helpers

This layer should absorb SQLAlchemy query details so services stay focused on business flow.

## 3. Scheduler Architecture
`backend/app/jobs/`

Current job split:
- `daily_price_job.py`
- `weekly_financial_job.py`
- `monthly_valuation_job.py`
- `alert_job.py` placeholder

Scheduler registration lives in:
- `backend/app/jobs/scheduler.py`

## 4. Upgrade Strategy
- Blank local DBs can still use `create_tables.py`.
- Existing environments should use Alembic migrations in `backend/alembic/`.
- The VI refactor is additive by design to preserve current API compatibility.
