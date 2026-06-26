# Personal US Stock Monitoring Platform & Quantitative Trading Cockpit

Backend and frontend for a personal US equity monitoring system with historical snapshots, internal value-investing metrics, intrinsic value estimates, and opportunity scoring.

## Stack
- Backend: FastAPI, Python 3.12+, SQLAlchemy 2.0, APScheduler
- Database: Supabase PostgreSQL
- Frontend: React, Vite, TypeScript, Tailwind CSS
- Providers: Yahoo Finance (`yfinance`), Finnhub, SEC EDGAR skeleton, FRED skeleton

## Raw-Data-First Architecture
The backend now follows this pipeline:

`Raw Data -> Normalization -> Metrics -> Valuation -> Scoring -> Dashboard`

Key backend areas:

```text
backend/app/
├── api/routes/         # Stocks, scores, refresh, metrics, valuation, statements
├── jobs/               # Daily, weekly, and monthly scheduler jobs
├── metrics/            # Internal VI math and metric engine
├── models/             # Raw, normalized, metric, valuation, and score snapshots
├── normalization/      # Yahoo/SEC mapping into normalized statement shapes
├── providers/          # Yahoo, Finnhub, SEC EDGAR skeleton, FRED skeleton
├── repositories/       # Append-only snapshot reads/writes
├── services/           # VI pipeline, stock scoring, ingestion compatibility wrapper
└── valuation/          # DCF, owner earnings, margin of safety, placeholders
```

The design remains append-only for statements, valuations, metrics, prices, and scores. Same-day recalculations are idempotent for scores and additive for raw snapshots.

## Main Data Models
- `raw_api_responses`
- `raw_financial_statements`
- `normalized_income_statements`
- `normalized_balance_sheets`
- `normalized_cash_flow_statements`
- `financial_metrics`
- `intrinsic_values`
- `macro_indicators`
- `stock_scores`

## API Overview
Existing routes remain:
- `GET /api/stocks`
- `GET /api/scores/latest`
- `GET /api/scores/top`
- `POST /api/refresh/{ticker}` -> compatibility alias to full VI refresh

New routes:
- `GET /api/metrics/{ticker}`
- `GET /api/valuation/{ticker}`
- `GET /api/statements/{ticker}?period_type=annual&limit=4`
- `POST /api/refresh/{ticker}/raw`
- `POST /api/refresh/{ticker}/full-vi`

## Backend Setup
From `backend/`:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and fill in the real values:

```env
PROJECT_NAME="Stock Monitor API"
ENVIRONMENT=development
SUPABASE_URL=postgresql://postgres.xxx:YOUR_PASSWORD@aws-0-xx-region.pooler.supabase.com:6543/postgres
FINNHUB_API_KEY=your_finnhub_api_key_here
FRED_API_KEY=
SEC_USER_AGENT="stock-monitor/1.0 your-email@example.com"
```

## Database Initialization
For a blank local database:

```bash
$env:PYTHONPATH="."
python create_tables.py
```

For existing databases, use Alembic from `backend/`:

```bash
$env:PYTHONPATH="."
alembic upgrade head
```

The included migrations assume an existing baseline schema, then apply the additive VI changes.

## Running the API
From `backend/`:

```bash
python -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`, with docs at `http://127.0.0.1:8000/docs`.

## Scheduler Jobs
- Daily price job: refresh raw market/analyst data and recalculate scores
- Weekly financial job: full VI refresh for active tickers
- Monthly valuation job: full VI refresh for valuation rebasing
- Alert job: placeholder only

## Tests
From `backend/`:

```bash
python -m pytest -q
```

Current coverage includes:
- safe division
- CAGR
- FCF calculation
- ROIC calculation
- DCF valuation
- margin of safety
- opportunity score weighting
- Yahoo statement normalization
- partial-success pipeline behavior
- refresh route response shape
