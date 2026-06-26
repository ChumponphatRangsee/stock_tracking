from math import pow
from typing import Optional


def safe_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_divide(numerator, denominator, default: float = 0.0) -> float:
    num = safe_float(numerator)
    den = safe_float(denominator)
    if num is None or den in (None, 0.0):
        return default
    return num / den


def calculate_cagr(start_value, end_value, periods: int, default: float = 0.0) -> float:
    start = safe_float(start_value)
    end = safe_float(end_value)
    if start is None or end is None or start <= 0 or end <= 0 or periods <= 0:
        return default
    return pow(end / start, 1 / periods) - 1


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))
