def calculate_quality_score(
    roe: float, 
    roic: float, 
    ebit_margin: float, 
    debt_equity: float, 
    rev_growth: float, 
    ebit_growth: float
) -> float:
    """
    Quality score built from internally calculated statement metrics.
    """
    score = 0.0
    
    if roic is not None:
        if roic >= 0.20: score += 25
        elif roic > 0.15: score += 20
        elif roic > 0.10: score += 15
        elif roic > 0.05: score += 10
        
    elif roe is not None:
        if roe >= 0.25: score += 25
        elif roe > 0.15: score += 20
        elif roe > 0.10: score += 15
        elif roe > 0.05: score += 10

    if ebit_margin is not None:
        if ebit_margin >= 0.25: score += 20
        elif ebit_margin > 0.15: score += 15
        elif ebit_margin > 0.10: score += 10
        elif ebit_margin > 0.05: score += 5

    if debt_equity is not None:
        if debt_equity <= 0.5: score += 20
        elif debt_equity <= 1.0: score += 15
        elif debt_equity <= 1.5: score += 10
        elif debt_equity <= 2.0: score += 5

    if ebit_growth is not None:
        if ebit_growth >= 0.20: score += 20
        elif ebit_growth > 0.10: score += 15
        elif ebit_growth > 0.05: score += 10
        elif ebit_growth > 0.0: score += 5
    elif rev_growth is not None:
        if rev_growth >= 0.20: score += 20
        elif rev_growth > 0.10: score += 15
        elif rev_growth > 0.05: score += 10
        elif rev_growth > 0.0: score += 5

    if rev_growth is not None and ebit_growth is not None:
        if rev_growth > 0 and ebit_growth > 0:
            score += 15
        elif rev_growth > 0 or ebit_growth > 0:
            score += 7

    return min(score, 100.0)
