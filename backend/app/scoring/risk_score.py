def calculate_risk_score(
    debt_to_equity: float,
    revenue_growth_1y: float,
    ebit_growth_3y_cagr: float,
    fcf_growth_3y_cagr: float,
    fcf_margin: float,
    share_dilution_pct: float,
) -> float:
    score = 0.0

    if debt_to_equity is not None:
        if debt_to_equity > 2.0: score += 25
        elif debt_to_equity > 1.0: score += 15
        elif debt_to_equity > 0.5: score += 8

    if revenue_growth_1y is not None and revenue_growth_1y < 0:
        score += 15

    if ebit_growth_3y_cagr is not None and ebit_growth_3y_cagr < 0:
        score += 15

    if fcf_growth_3y_cagr is not None and fcf_growth_3y_cagr < 0:
        score += 15

    if fcf_margin is not None and fcf_margin < 0:
        score += 20

    if share_dilution_pct is not None:
        if share_dilution_pct > 0.15: score += 10
        elif share_dilution_pct > 0.05: score += 5

    score += 5
    return min(score, 100.0)
