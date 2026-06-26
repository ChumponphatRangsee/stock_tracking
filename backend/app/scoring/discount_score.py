def calculate_discount_score(below_52w_high_pct: float) -> float:
    """
    Score out of 100 based on the drawdown from 52-week high.
    This identifies "Quality on Sale".
    
    Expected input: a positive percentage representing the drop (e.g. 25.0 for a 25% drop).
    """
    if not below_52w_high_pct or below_52w_high_pct <= 0:
        return 0.0
        
    score = 0.0
    
    # We want a healthy discount (margin of safety) but not a complete collapse (which indicates distress).
    # Sweet spot is a 15% - 40% pullback for healthy, high-quality companies.
    if 15.0 <= below_52w_high_pct <= 35.0:
        score = 100.0
    elif 10.0 <= below_52w_high_pct < 15.0:
        score = 80.0
    elif 35.0 < below_52w_high_pct <= 50.0:
        score = 70.0
    elif 5.0 <= below_52w_high_pct < 10.0:
        score = 40.0
    elif below_52w_high_pct > 50.0:
        # Pullbacks over 50% for huge companies usually mean something is fundamentally broken
        score = 30.0
    else:
        # Pullbacks under 5% provide little discount incentive
        score = 10.0
        
    return score
