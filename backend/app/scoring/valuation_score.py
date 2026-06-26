def calculate_valuation_score(
    fcf_yield: float,
    earnings_yield: float,
    ev_ebit: float,
    ev_fcf: float,
) -> float:
    """
    Valuation score from internally calculated yields and enterprise value multiples.
    """
    score = 0.0
    
    if fcf_yield is not None:
        if fcf_yield >= 0.08: score += 30
        elif fcf_yield >= 0.05: score += 22
        elif fcf_yield >= 0.03: score += 15
        elif fcf_yield > 0.0: score += 8

    if earnings_yield is not None:
        if earnings_yield >= 0.08: score += 25
        elif earnings_yield >= 0.05: score += 20
        elif earnings_yield >= 0.03: score += 12
        elif earnings_yield > 0.0: score += 6

    if ev_ebit is not None and ev_ebit > 0:
        if ev_ebit <= 8: score += 25
        elif ev_ebit <= 12: score += 20
        elif ev_ebit <= 16: score += 14
        elif ev_ebit <= 22: score += 8

    if ev_fcf is not None and ev_fcf > 0:
        if ev_fcf <= 10: score += 20
        elif ev_fcf <= 15: score += 15
        elif ev_fcf <= 20: score += 10
        elif ev_fcf <= 30: score += 5

    return min(score, 100.0)
