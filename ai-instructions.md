# AI Coding & System Instructions - Stock Monitor Platform

This document is the working instruction set for AI assistants operating in this repository.

## 1. Project Philosophy
The platform is now a raw-data-first value-investing system.

Core rule:
- Store raw provider payloads first.
- Normalize statements into internal schemas.
- Calculate metrics internally from normalized data.
- Calculate intrinsic values from internal metrics.
- Score stocks from internal metrics and valuations.

Do not design new features around prebuilt vendor ratios unless they are clearly marked as supplemental only.

## 2. Snapshot and Persistence Rules
- Use append-only storage for raw responses, raw statements, normalized statements, intrinsic values, macro indicators, metrics, prices, analyst data, and score snapshots.
- Never destructively overwrite historical rows.
- Use `snapshot_date`, `price_date`, `period_end_date`, `valuation_date`, or `fetched_at` as the historical anchor.
- Same-day score recalculation may upsert the same `(ticker, snapshot_date, score_version)` score row, but raw and statement data should remain additive.

## 3. Backend Architecture

| Folder Path | Responsibility |
| :--- | :--- |
| `backend/app/api/routes/` | FastAPI routes and response contracts |
| `backend/app/providers/` | External provider adapters: Yahoo, Finnhub, SEC EDGAR skeleton, FRED skeleton |
| `backend/app/ingestion/` | Raw/price/statement/analyst/macro ingestion helpers |
| `backend/app/normalization/` | Provider-specific statement normalization into internal schemas |
| `backend/app/metrics/` | Pure internal metric calculations |
| `backend/app/valuation/` | DCF, owner earnings, margin of safety, placeholders |
| `backend/app/scoring/` | Pure scoring functions |
| `backend/app/repositories/` | Database read/write helpers |
| `backend/app/services/` | Pipeline orchestration and business services |
| `backend/app/models/` | SQLAlchemy ORM models |
| `backend/app/jobs/` | Scheduler job entrypoints |
| `backend/alembic/` | Database migrations |

Primary orchestration path:

`provider fetch -> raw storage -> normalization -> metrics -> valuation -> scoring -> API`

Main service entrypoint:
- `backend/app/services/vi_pipeline_service.py`

Compatibility wrapper:
- `backend/app/services/data_ingestion_service.py`

## 4. Provider Rules
- Yahoo is the primary v1 source for raw profile, quote, statement, and supplemental target/multiple data.
- Finnhub is used for analyst recommendation trends.
- SEC EDGAR is additive enrichment/fallback, not the primary statement source in v1.
- FRED is used for macro indicators.
- Do not hardcode API keys or SEC headers.
- SEC requests must use `SEC_USER_AGENT`.
- Respect quota and throttling rules through `QuotaService` and the provider layer.

## 5. Metric and Valuation Rules
- Prefer internal calculations from normalized statements over vendor ratios.
- Use safe math helpers from `backend/app/utils/math_utils.py`.
- Keep calculations deterministic and Python-native. Do not pass NumPy scalar types into ORM writes.
- Use vendor values like `forward_pe`, `pe_ratio`, `ps_ratio`, and `peg_ratio` only as supplemental fields, not as the core value-investing data source.
- Current implemented valuation methods:
  - DCF
  - Owner earnings
- Current placeholder methods:
  - Reverse DCF
  - EPV

## 6. Database and Migration Rules
- Use `SessionLocal` from `app.core.database` in jobs and service code.
- Use `db: Session = Depends(get_db)` in routes.
- For existing databases, schema changes should go through Alembic.
- `create_tables.py` is acceptable for blank local databases, not as a replacement for migrations on real upgrades.

## 7. File and Encoding Rules
- Keep config and documentation files in UTF-8.
- Do not write UTF-16 `.env` files.
- Prefer ASCII content in code and docs unless a file already requires otherwise.

## 8. How to Extend the System
- To add a new normalized field:
  - update the normalized model
  - update the relevant mapper/normalizer
  - update downstream metric or valuation consumers
- To add a new metric:
  - update `models/financial_metric.py`
  - update `metrics/`
  - update pipeline persistence
  - update scoring if needed
- To add a new provider:
  - add the adapter in `providers/`
  - register it in `ProviderFactory`
  - define where it fits in the raw-data-first pipeline
- To add a new API:
  - expose it in `api/routes/`
  - prefer repository or service access over direct route-side SQL when behavior is non-trivial

## 9. What Not To Reintroduce
- Do not move the system back to vendor-ratio-first architecture.
- Do not couple scoring directly to Yahoo-only metrics extraction.
- Do not bypass normalization when introducing new statement-driven metrics.
- Do not replace append-only raw storage with overwrite-in-place behavior.
