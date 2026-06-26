def calculate_quality_score(
    roe: float, 
    roic: float, 
    ebit_margin: float, 
    debt_equity: float, 
    rev_growth: float, 
    ebit_growth: float
) -> float:
    """
    Quality Score (out of 100).
    Evaluates business efficiency, profitability, leverage, and core growth.
    """
    score = 0.0
    
    # 1. ROIC (Return on Invested Capital) - up to 25 points
    # Represents the true efficiency of capital allocation
    if roic is not None:
        if roic >= 0.20: score += 25
        elif roic > 0.15: score += 20
        elif roic > 0.10: score += 15
        elif roic > 0.05: score += 10
        
    # Fallback to ROE if ROIC is missing
    elif roe is not None:
        if roe >= 0.25: score += 25
        elif roe > 0.15: score += 20
        elif roe > 0.10: score += 15
        elif roe > 0.05: score += 10

    # 2. EBIT Margin (Operating Margin) - up to 20 points
    # Measures the pricing power and operational efficiency
    if ebit_margin is not None:
        if ebit_margin >= 0.25: score += 20
        elif ebit_margin > 0.15: score += 15
        elif ebit_margin > 0.10: score += 10
        elif ebit_margin > 0.05: score += 5

    # 3. Debt to Equity (Leverage Strength) - up to 20 points
    # Lower debt is better. Note: yfinance presents Debt/Equity as a percentage (e.g. 79.5 means 79.5%)
    if debt_equity is not None:
        if debt_equity <= 50.0: score += 20
        elif debt_equity <= 100.0: score += 15
        elif debt_equity <= 150.0: score += 10
        elif debt_equity <= 200.0: score += 5

    # 4. EBIT Growth (Core Operating Profit Growth) - up to 20 points
    if ebit_growth is not None:
        if ebit_growth >= 0.20: score += 20
        elif ebit_growth > 0.10: score += 15
        elif ebit_growth > 0.05: score += 10
        elif ebit_growth > 0.0: score += 5
    # Fallback to top-line Revenue Growth
    elif rev_growth is not None:
        if rev_growth >= 0.20: score += 20
        elif rev_growth > 0.10: score += 15
        elif rev_growth > 0.05: score += 10
        elif rev_growth > 0.0: score += 5

    # 5. Profit Margin / Growth consistency bonus - up to 15 points
    if rev_growth is not None and ebit_growth is not None:
        if rev_growth > 0 and ebit_growth > 0:
            score += 15
        elif rev_growth > 0 or ebit_growth > 0:
            score += 7

    return min(score, 100.0)
