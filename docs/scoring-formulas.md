# Scoring Formulas & Business Logic Specification

This document details the exact quantitative scoring strategies executed by the platform's **Modular Opportunity Scoring Engine** in `backend/app/scoring/`.

---

## 1. Quality Score (Max: 100)
*   **Formula File:** `backend/app/scoring/quality_score.py`
*   **Purpose:** Measures structural business quality, return efficiency, profit margin strength, balance sheet risk, and operating profitability growth.

### Score Metrics allocation:

1.  **ROIC (Return on Invested Capital) - Weight: 25 Points**
    *   *ROIC >= 20%:* **25 Points**
    *   *ROIC > 15%:* **20 Points**
    *   *ROIC > 10%:* **15 Points**
    *   *ROIC > 5%:* **10 Points**
    *   *Fallback (ROE if ROIC is missing):* Same brackets scaled down to a max of **20 Points** for ROE.
2.  **EBIT Margin (Operating Profitability) - Weight: 20 Points**
    *   *Margin >= 25%:* **20 Points**
    *   *Margin > 15%:* **15 Points**
    *   *Margin > 10%:* **10 Points**
    *   *Margin > 5%:* **5 Points**
3.  **Debt-to-Equity (Balance Sheet Strength) - Weight: 20 Points**
    *   *Ratio <= 50%:* **20 Points** (Very healthy/low leverage)
    *   *Ratio <= 100%:* **15 Points** (Acceptable leverage)
    *   *Ratio <= 150%:* **10 Points** (Moderate risk)
    *   *Ratio <= 200%:* **5 Points** (High leverage)
    *   *Ratio > 200%:* **0 Points**
4.  **EBIT Growth (Core Profit Momentum) - Weight: 20 Points**
    *   *EBIT Growth >= 20%:* **20 Points**
    *   *EBIT Growth > 10%:* **15 Points**
    *   *EBIT Growth > 5%:* **10 Points**
    *   *EBIT Growth > 0%:* **5 Points**
    *   *Fallback (Revenue Growth if EBIT Growth is missing):* Matches same brackets.
5.  **Growth Consistency Bonus - Weight: 15 Points**
    *   If both Revenue Growth and EBIT Growth are positive (expansion phase): **+15 Points**.
    *   If only one of them is positive: **+7 Points**.

---

## 2. Valuation Score (Max: 100)
*   **Formula File:** `backend/app/scoring/valuation_score.py`
*   **Purpose:** Identifies if a stock is cheap, reasonably priced, or overvalued compared to its current earnings, future prospects, and sales.

### Score Metrics allocation:

1.  **P/E Multiple (Forward P/E prioritized over Trailing P/E) - Weight: 45 Points**
    *   *P/E < 12.0:* **45 Points**
    *   *P/E < 18.0:* **35 Points**
    *   *P/E < 25.0:* **25 Points**
    *   *P/E < 32.0:* **15 Points**
    *   *P/E < 40.0:* **5 Points**
2.  **PEG Ratio (Price/Earnings Relative to Growth) - Weight: 35 Points**
    *   *PEG <= 1.0:* **35 Points** (Extremely cheap growth)
    *   *PEG <= 1.5:* **25 Points**
    *   *PEG <= 2.0:* **15 Points**
    *   *PEG <= 3.0:* **5 Points**
    *   *Fallback:* If PEG is missing, but P/E is < 20, give a **15 Points** default buffer.
3.  **P/S Multiple (Price-to-Sales) - Weight: 20 Points**
    *   *P/S < 1.5:* **20 Points**
    *   *P/S < 3.0:* **15 Points**
    *   *P/S < 5.0:* **10 Points**
    *   *P/S < 8.0:* **5 Points**

---

## 3. Discount Score (Max: 100)
*   **Formula File:** `backend/app/scoring/discount_score.py`
*   **Purpose:** Measures the "On Sale" discount from the 52-week high, looking for high-quality pullbacks while avoiding collapsing "falling knives."

### Score Metrics allocation:
*   **Pullback between 15% and 35% (The Sweet Spot):** **100 Points**
*   **Pullback between 10% and 15%:** **80 Points**
*   **Pullback between 35% and 50%:** **70 Points**
*   **Pullback between 5% and 10%:** **40 Points**
*   **Pullback over 50% (Distressed Asset Risk):** **30 Points**
*   **Pullback under 5%:** **10 Points**

---

## 4. Analyst Score (Max: 100)
*   **Formula File:** `backend/app/scoring/analyst_score.py`
*   **Purpose:** Measures the Wall Street consensus ratings and target price upsides.

### Score Metrics allocation:

1.  **Price Target Upside Percentage - Weight: 50 Points**
    *   *Upside >= 30%:* **50 Points**
    *   *Upside >= 20%:* **40 Points**
    *   *Upside >= 15%:* **30 Points**
    *   *Upside >= 10%:* **20 Points**
    *   *Upside >= 5%:* **10 Points**
    *   *Upside > 0%:* **5 Points**
2.  **Bullish Recommendations Ratio - Weight: 50 Points**
    *   Calculates the ratio: `(Strong Buy + Buy) / Total Recommendations`
    *   *Score:* `Ratio * 50.0` points (e.g. if 80% of ratings are Buy/Strong Buy, stock receives **40 Points**).

---

## 5. Master Opportunity Score (Max: 100)
*   **Formula File:** `backend/app/scoring/opportunity_score.py`
*   **Purpose:** The single, definitive metric that combines all 4 dimensions.

$$OpportunityScore = 40\% \times Quality + 30\% \times Valuation + 20\% \times Discount + 10\% \times Analyst$$
