def calculate_analyst_score(
    target_upside_pct: float, 
    strong_buy: int, 
    buy: int, 
    hold: int, 
    sell: int, 
    strong_sell: int
) -> float:
    """
    Analyst Score (out of 100).
    Evaluates wall-street price targets and the bullish/bearish recommendation ratios.
    """
    score = 0.0
    
    # 1. Price Target Upside - up to 50 points
    if target_upside_pct is not None:
        if target_upside_pct >= 30.0: score += 50
        elif target_upside_pct >= 20.0: score += 40
        elif target_upside_pct >= 15.0: score += 30
        elif target_upside_pct >= 10.0: score += 20
        elif target_upside_pct >= 5.0: score += 10
        elif target_upside_pct > 0: score += 5

    # 2. Bullish Consensus Ratio - up to 50 points
    total_recs = strong_buy + buy + hold + sell + strong_sell
    if total_recs > 0:
        bullish_recs = strong_buy + buy
        bullish_ratio = bullish_recs / total_recs
        score += (bullish_ratio * 50.0)
        
    return min(score, 100.0)
