def calculate_opportunity_score(
    quality_score: float,
    valuation_score: float,
    discount_score: float,
    analyst_score: float
) -> float:
    """
    Calculates the final opportunity score based on weighted metrics.
    Formula: 
    - 40% Quality Score (To ensure the company is structurally sound)
    - 30% Valuation Score (To ensure we aren't overpaying)
    - 20% Discount Score (To measure the 'on sale' factor)
    - 10% Analyst Score (Wall street consensus indicator)
    """
    # Ensure no None types break the mathematical formula
    q = quality_score if quality_score is not None else 0.0
    v = valuation_score if valuation_score is not None else 0.0
    d = discount_score if discount_score is not None else 0.0
    a = analyst_score if analyst_score is not None else 0.0

    q_weight = 0.40
    v_weight = 0.30
    d_weight = 0.20
    a_weight = 0.10

    opp_score = (
        (q * q_weight) +
        (v * v_weight) +
        (d * d_weight) +
        (a * a_weight)
    )
    
    return round(opp_score, 2)
