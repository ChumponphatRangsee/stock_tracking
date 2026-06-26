# Database Schema & Snapshot Strategy Documentation

This document summarizes the current snapshot-oriented schema after the raw-data-first value-investing refactor.

## 1. Snapshot Strategy
- Prices, analyst data, metrics, valuations, macro indicators, raw responses, raw statements, and normalized statements are historical snapshots.
- Historical data should be appended, not replaced.
- Score rows may be recalculated for the same `ticker + snapshot_date + score_version`, but the intent remains historical traceability.

## 2. Core Tables

### A. Security Registry
- `stocks`
- `watchlists`

### B. Market and Analyst Snapshots
- `stock_prices`
- `analyst_data`
- `stock_scores`

### C. Raw Storage
- `raw_api_responses`
- `raw_financial_statements`

### D. Normalized Statements
- `normalized_income_statements`
- `normalized_balance_sheets`
- `normalized_cash_flow_statements`

### E. Internal Calculation Outputs
- `financial_metrics`
- `intrinsic_values`
- `macro_indicators`

### F. Operational Tables
- `api_request_queue`
- `api_usage_logs`

## 3. Important Table Shapes

### `raw_api_responses`
- `id`
- `provider`
- `endpoint`
- `ticker`
- `data_type`
- `raw_json`
- `data_hash`
- `fetched_at`
- `created_at`

### `raw_financial_statements`
- `id`
- `ticker`
- `provider`
- `statement_type`
- `fiscal_year`
- `fiscal_quarter`
- `period_end_date`
- `raw_json`
- `accession_number`
- `created_at`

### `normalized_income_statements`
Primary key:
- `ticker`
- `period_end_date`
- `period_type`

Important fields:
- `fiscal_year`
- `fiscal_quarter`
- `revenue`
- `gross_profit`
- `operating_income`
- `ebit`
- `net_income`
- `eps_basic`
- `eps_diluted`
- `shares_basic`
- `shares_diluted`

### `normalized_balance_sheets`
Primary key:
- `ticker`
- `period_end_date`
- `period_type`

Important fields:
- `cash_and_equivalents`
- `current_assets`
- `total_assets`
- `current_liabilities`
- `total_liabilities`
- `total_debt`
- `total_equity`
- `invested_capital`

### `normalized_cash_flow_statements`
Primary key:
- `ticker`
- `period_end_date`
- `period_type`

Important fields:
- `operating_cash_flow`
- `capital_expenditure`
- `free_cash_flow`
- `dividends_paid`
- `share_buybacks`

### `financial_metrics`
Primary key:
- `ticker`
- `snapshot_date`

Important fields include:
- vendor supplemental: `forward_pe`, `pe_ratio`, `ps_ratio`, `peg_ratio`
- growth: `revenue_growth_1y`, `revenue_growth_3y_cagr`, `ebit_growth_3y_cagr`, `fcf_growth_3y_cagr`
- profitability: `gross_margin`, `operating_margin`, `net_margin`, `fcf_margin`
- returns: `roe`, `roic`, `roce`, `croic`
- balance sheet: `debt_to_equity`, `net_debt_to_ebit`, `current_ratio`
- valuation metrics: `fcf_yield`, `earnings_yield`, `ev_ebit`, `ev_fcf`, `buyback_yield`
- capital structure: `share_dilution_pct`

### `intrinsic_values`
- `id`
- `ticker`
- `valuation_date`
- `method`
- `base_case_value`
- `bear_case_value`
- `bull_case_value`
- `assumptions_json`
- `margin_of_safety_pct`
- `created_at`

### `macro_indicators`
- `id`
- `indicator_name`
- `observation_date`
- `value`
- `source`
- `metadata_json`
- `created_at`

### `stock_scores`
Primary key:
- `ticker`
- `snapshot_date`
- `score_version`

Important fields:
- `quality_score`
- `valuation_score`
- `discount_score`
- `analyst_score`
- `trend_score`
- `risk_score`
- `margin_of_safety_score`
- `opportunity_score`

## 4. Key Relationships

```text
[stocks]
  ├── [stock_prices]
  ├── [analyst_data]
  ├── [financial_metrics]
  ├── [intrinsic_values]
  ├── [stock_scores]
  ├── [raw_financial_statements]
  ├── [normalized_income_statements]
  ├── [normalized_balance_sheets]
  └── [normalized_cash_flow_statements]
```

`raw_api_responses` may reference a ticker, but it is primarily an audit/cache table and not a normalized financial relation.

## 5. Migration Notes
- The repository now includes Alembic for schema upgrades.
- Existing deployments should be migrated via Alembic, not by relying only on `Base.metadata.create_all`.
- `create_tables.py` remains useful for blank local environments.
