# API Request Strategy & Provider Mapping

This document describes the current provider usage strategy for the raw-data-first backend.

## 1. Provider Roles

### Yahoo Finance
Primary v1 provider for:
- company profile
- quote and 52-week range
- raw income statements
- raw balance sheets
- raw cash flow statements
- supplemental vendor fields such as `forward_pe`, `pe_ratio`, `ps_ratio`, `peg_ratio`
- analyst target prices from `info`

Yahoo is the primary statement source in v1, but normalized metrics should still be calculated internally after raw ingestion.

### Finnhub
Used for:
- analyst recommendation trends

Finnhub is not the primary source for financial statements or valuation metrics.

### SEC EDGAR
Used for:
- ticker to CIK mapping
- company facts skeleton
- future enrichment and fallback paths

SEC is additive in v1, not the default source of normalized statements.

### FRED
Used for:
- treasury yield
- federal funds rate
- CPI / inflation series
- unemployment rate

## 2. Data Mapping by Layer

### Raw Layer
- store provider payloads in `raw_api_responses`
- store raw statement rows in `raw_financial_statements`

### Normalization Layer
- Yahoo raw statements are mapped into:
  - `normalized_income_statements`
  - `normalized_balance_sheets`
  - `normalized_cash_flow_statements`

### Metrics Layer
Calculated internally from normalized statements:
- FCF
- ROIC
- ROE
- ROCE
- CROIC
- margins
- growth rates and CAGR metrics
- debt and liquidity ratios
- valuation yields and EV multiples
- share dilution

### Valuation Layer
Calculated internally:
- DCF
- owner earnings value
- margin of safety

Placeholder only in v1:
- reverse DCF
- EPV

### Scoring Layer
Calculated internally:
- quality
- valuation
- trend
- risk
- analyst
- margin of safety
- opportunity

## 3. Quota and Safety Rules
- Do not fetch all provider data from request/response endpoints unless the route is explicitly a refresh path.
- Prefer scheduled jobs and refresh endpoints for provider access.
- SEC requests must include `SEC_USER_AGENT`.
- Use provider throttling and quota accounting through the existing service/provider stack.
- Do not reintroduce paid-provider assumptions into the default architecture.

## 4. Practical Rule for New Features
When adding a new investing metric:
1. fetch or reuse raw provider data
2. persist raw data if it is new
3. normalize into internal shape if statement-driven
4. calculate the metric internally
5. expose it via repositories, services, and APIs as needed

Do not skip directly from provider payload to score logic unless the field is explicitly supplemental.
