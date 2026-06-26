def calculate_trend_score(
    revenue_growth_3y_cagr: float,
    ebit_growth_3y_cagr: float,
    fcf_growth_3y_cagr: float,
    operating_margin: float,
    fcf_margin: float,
) -> float:
    score = 0.0
    growth_values = [revenue_growth_3y_cagr, ebit_growth_3y_cagr, fcf_growth_3y_cagr]
    for value in growth_values:
        if value is None:
            continue
        if value >= 0.15:
            score += 20
        elif value >= 0.08:
            score += 14
        elif value > 0:
            score += 8
        else:
            score += 2

    if operating_margin is not None:
        if operating_margin >= 0.20:
            score += 20
        elif operating_margin >= 0.10:
            score += 12
        elif operating_margin > 0:
            score += 6

    if fcf_margin is not None:
        if fcf_margin >= 0.15:
            score += 20
        elif fcf_margin >= 0.08:
            score += 14
        elif fcf_margin > 0:
            score += 8

    return min(score, 100.0)
