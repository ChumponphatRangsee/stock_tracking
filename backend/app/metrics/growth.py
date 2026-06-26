from app.utils.math_utils import calculate_cagr, safe_divide


def calculate_growth(current_value, previous_value) -> float:
    previous = float(previous_value or 0.0)
    if previous == 0.0:
        return 0.0
    return safe_divide(float(current_value or 0.0) - previous, abs(previous))


def calculate_three_year_cagr(current_value, prior_three_year_value) -> float:
    return calculate_cagr(prior_three_year_value, current_value, 3)
