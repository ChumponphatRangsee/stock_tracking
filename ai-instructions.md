# AI Coding & System Instructions - Stock Monitor Platform

This document serves as the master instruction set ("System Prompt Extension") for any AI assistant or LLM agent (like Cursor, Claude, or ChatGPT) working on this codebase. 

---

## 1. Project Overview & Core Philosophy
The **Personal Stock Monitor Platform** is a quantitative screening and trend analysis tool designed to track US stocks, calculate deep operational quality and valuation scores, and highlight "Quality Stocks on Sale."

*   **Strict No-Overwrite Snapshot Rule:** The system uses an **append-only/historical snapshot strategy** for all time-series tables (`stock_prices`, `financial_metrics`, `analyst_data`, and `stock_scores`). 
    *   *Never* overwrite an existing row for a stock.
    *   *Always* insert a new row with `snapshot_date` or `price_date`.
    *   *Reason:* This allows historical score tracking, sector trend analysis, and backtesting.
*   **API Quota Constraint:** The platform operates under tight Free Tier limits (primarily Yahoo Finance for fundamentals/targets and Finnhub for recommendations). 
    *   Do *not* write loops that fetch raw data on every API endpoint every day.
    *   Utilize background queues, delta checks, and daily/weekly rolling updates.

---

## 2. Tech Stack Core Settings

*   **Backend:** FastAPI (Python 3.12+), SQLAlchemy 2.0 (ORM), Background APScheduler.
*   **Database:** Supabase PostgreSQL.
*   **Primary Data Provider:** Yahoo Finance via `yfinance` python library (for quotes, profiles, targets, balance sheet ratios, ROIC, and EBIT growth).
*   **Secondary Data Provider:** Finnhub (strictly for monthly Recommendation Trends to prevent 403/429 limits).
*   **Frontend:** React (Vite, TypeScript), Tailwind CSS, Recharts, TanStack Table.

---

## 3. Architecture Blueprint & Code Locations

Enforce the following Domain-Driven Design (DDD) rules when writing or modifying code:

| Folder Path | Layer Name | Responsibility |
| :--- | :--- | :--- |
| `backend/app/api/routes/` | **Controller** | Exposes HTTP REST endpoints. Handles inputs via Pydantic Schemas. |
| `backend/app/providers/` | **Adapters** | Interface for third-party APIs. Translates provider raw data to unified schemas. |
| `backend/app/services/` | **Domain Services** | Coordinates ingestion pipelines, quota accounting, and calculations. |
| `backend/app/scoring/` | **Domain Entities** | Math modules containing the scoring strategies. Free of side-effects. |
| `backend/app/repositories/` | **Infrastructure** | SQL-only wrapper layer utilizing SQLAlchemy queries. |
| `backend/app/models/` | **Database Schemas** | SQLAlchemy ORM structural database models. |
| `backend/app/schemas/` | **Data Validation** | Pydantic Models for API translation (request/response). |
| `backend/app/jobs/` | **Background Jobs** | APScheduler background worker cron task runners. |

---

## 4. Coding Rules for AI Assistants

### A. Database Connections
*   Always use `SessionLocal` from `app.core.database` for thread-safe database operations.
*   In API routes, inject the session via `db: Session = Depends(get_db)`.
*   In background workers (`app/jobs/`), manually instantiate `db = SessionLocal()` inside a `try...finally: db.close()` block to prevent connection leakage.

### B. Special Numeric Data Handling (NumPy/Pandas)
*   Because `yfinance` depends on Pandas and NumPy, values can occasionally return as numpy scalars (e.g. `np.float64`).
*   **Rule:** Always pass numeric variables fetched from Yahoo through the `self._to_native_float()` method inside the provider layer before passing them to SQLAlchemy models to prevent SQL compilation crashes.

### C. File Encoding
*   Ensure all configuration files (especially `.env` and `.env.example`) are written and saved with **UTF-8 (no BOM)** encoding. Never write UTF-16 configurations.

### D. Extending the Platform
*   **To add a new Metric:** First update the model in `models/financial_metric.py`, update `providers/yahoo/yahoo_provider.py` to extract it, and then modify the scoring strategy in `scoring/`.
*   **To add a new API Provider:** Implement the abstract base classes in `providers/base/` and add the provider class into the factory pattern in `providers/provider_factory.py`.
