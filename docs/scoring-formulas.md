# Scoring Formulas & Business Logic Specification

This document describes the currently implemented scoring behavior in `backend/app/scoring/`.

## 1. Quality Score
File:
- `backend/app/scoring/quality_score.py`

Purpose:
- measure business quality using internally calculated return, leverage, and growth metrics

Current inputs:
- `roe`
- `roic`
- `ebit_margin` or `operating_margin`
- `debt_to_equity`
- revenue growth
- EBIT growth

High-level behavior:
- rewards strong ROIC or ROE
- rewards strong operating margins
- rewards low leverage
- rewards positive operating growth
- adds a consistency bonus when both revenue and EBIT growth are positive

## 2. Valuation Score
File:
- `backend/app/scoring/valuation_score.py`

Purpose:
- rank relative cheapness using internally derived valuation metrics

Current inputs:
- `fcf_yield`
- `earnings_yield`
- `ev_ebit`
- `ev_fcf`

High-level behavior:
- rewards higher free-cash-flow yield
- rewards higher earnings yield
- rewards lower EV/EBIT
- rewards lower EV/FCF

## 3. Discount Score
File:
- `backend/app/scoring/discount_score.py`

Purpose:
- preserve the legacy 52-week pullback signal for compatibility

Current role:
- still calculated and stored
- not part of the new opportunity score weighting

## 4. Analyst Score
File:
- `backend/app/scoring/analyst_score.py`

Purpose:
- capture target upside and recommendation mix

Current inputs:
- `target_upside_pct`
- `strong_buy`
- `buy`
- `hold`
- `sell`
- `strong_sell`

## 5. Trend Score
File:
- `backend/app/scoring/trend_score.py`

Purpose:
- measure multi-year operating and free-cash-flow direction

Current inputs:
- `revenue_growth_3y_cagr`
- `ebit_growth_3y_cagr`
- `fcf_growth_3y_cagr`
- `operating_margin`
- `fcf_margin`

High-level behavior:
- rewards positive multi-year growth
- rewards stronger operating margin
- rewards stronger free-cash-flow margin

## 6. Risk Score
File:
- `backend/app/scoring/risk_score.py`

Purpose:
- penalize balance sheet and business deterioration risks

Current inputs:
- `debt_to_equity`
- `revenue_growth_1y`
- `ebit_growth_3y_cagr`
- `fcf_growth_3y_cagr`
- `fcf_margin`
- `share_dilution_pct`

High-level behavior:
- increases risk for high leverage
- increases risk for declining revenue, EBIT, or FCF
- increases risk for negative FCF margin
- increases risk for share dilution
- includes a placeholder base risk component

## 7. Margin of Safety Score
File:
- `backend/app/scoring/margin_of_safety_score.py`

Purpose:
- convert intrinsic value discount into a score

Current input:
- `margin_of_safety_pct`

High-level behavior:
- higher margin of safety yields a higher score
- overvalued names receive low scores

## 8. Opportunity Score
File:
- `backend/app/scoring/opportunity_score.py`

Current implemented weighting:

```text
Opportunity Score =
  35% Quality
  25% Valuation
  15% Margin of Safety
  10% Trend
  10% Inverted Risk
   5% Analyst
```

Notes:
- risk is inverted in the final combination, so lower risk improves the score
- discount score is stored separately for compatibility and UI continuity, but is no longer part of the opportunity formula

## 9. Design Principle
- Metrics should come from normalized statements whenever possible.
- Scoring functions should remain pure and side-effect free.
- Provider-specific extraction logic should stay outside the scoring layer.
