def calculate_margin_of_safety_score(margin_of_safety_pct: float) -> float:
    if margin_of_safety_pct is None:
        return 0.0
    if margin_of_safety_pct >= 0.40:
        return 100.0
    if margin_of_safety_pct >= 0.25:
        return 80.0
    if margin_of_safety_pct >= 0.15:
        return 60.0
    if margin_of_safety_pct > 0:
        return 40.0
    if margin_of_safety_pct > -0.15:
        return 20.0
    return 0.0
