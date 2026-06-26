from app.utils.math_utils import safe_divide


def calculate_margin_of_safety(current_price: float, intrinsic_value: float) -> float:
    if not intrinsic_value:
        return 0.0
    return safe_divide(intrinsic_value - current_price, intrinsic_value)
