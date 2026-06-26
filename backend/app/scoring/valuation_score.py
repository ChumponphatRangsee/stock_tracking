def calculate_valuation_score(
    forward_pe: float, 
    pe_ratio: float, 
    ps_ratio: float, 
    peg_ratio: float
) -> float:
    """
    Valuation Score (out of 100).
    Rewards companies trading at cheaper, reasonable earnings and sales multiples.
    Negative or zero multiples are treated as unprofitable/unstable and receive 0.
    """
    score = 0.0
    
    # We prioritize Forward P/E (forward expectations) over Trailing P/E
    pe_to_use = forward_pe if forward_pe is not None else pe_ratio
    
    # 1. Price-to-Earnings (P/E) Multiple - up to 45 points
    if pe_to_use is not None and pe_to_use > 0:
        if pe_to_use < 12.0: score += 45
        elif pe_to_use < 18.0: score += 35
        elif pe_to_use < 25.0: score += 25
        elif pe_to_use < 32.0: score += 15
        elif pe_to_use < 40.0: score += 5

    # 2. PEG Ratio (P/E relative to growth) - up to 35 points
    # A PEG under 1.0 is considered the holy grail of valuation (undervalued relative to growth)
    if peg_ratio is not None and peg_ratio > 0:
        if peg_ratio <= 1.0: score += 35
        elif peg_ratio <= 1.5: score += 25
        elif peg_ratio <= 2.0: score += 15
        elif peg_ratio <= 3.0: score += 5
    else:
        # If PEG is missing, allocate points back to P/E or use default
        if pe_to_use is not None and pe_to_use < 20.0:
            score += 15

    # 3. Price-to-Sales (P/S) Multiple - up to 20 points
    if ps_ratio is not None and ps_ratio > 0:
        if ps_ratio < 1.5: score += 20
        elif ps_ratio < 3.0: score += 15
        elif ps_ratio < 5.0: score += 10
        elif ps_ratio < 8.0: score += 5

    return min(score, 100.0)
