def calculate_opportunity_score(
    quality_score: float,
    valuation_score: float,
    margin_of_safety_score: float,
    trend_score: float,
    risk_score: float,
    analyst_score: float,
) -> float:
    """
    Calculates the final opportunity score using the raw-data-first VI weighting.
    """
    q = quality_score if quality_score is not None else 0.0
    v = valuation_score if valuation_score is not None else 0.0
    m = margin_of_safety_score if margin_of_safety_score is not None else 0.0
    t = trend_score if trend_score is not None else 0.0
    risk = risk_score if risk_score is not None else 100.0
    a = analyst_score if analyst_score is not None else 0.0

    opp_score = (
        (q * 0.35) +
        (v * 0.25) +
        (m * 0.15) +
        (t * 0.10) +
        ((100.0 - risk) * 0.10) +
        (a * 0.05)
    )
    
    return round(opp_score, 2)
