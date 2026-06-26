from app.metrics.capital_allocation import calculate_roic
from app.metrics.cash_flow import calculate_free_cash_flow
from app.utils.math_utils import calculate_cagr, safe_divide


def test_safe_divide_handles_zero():
    assert safe_divide(10, 0) == 0.0


def test_cagr_returns_expected_value():
    result = calculate_cagr(100, 133.1, 3)
    assert round(result, 4) == 0.1


def test_fcf_calculation():
    assert calculate_free_cash_flow(120, -20) == 100.0


def test_roic_calculation():
    assert round(calculate_roic(79, 395), 4) == 0.2
