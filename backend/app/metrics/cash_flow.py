from app.utils.math_utils import safe_divide


def calculate_free_cash_flow(operating_cash_flow, capital_expenditure) -> float:
    return (float(operating_cash_flow or 0.0)) - abs(float(capital_expenditure or 0.0))


def calculate_fcf_margin(free_cash_flow, revenue) -> float:
    return safe_divide(free_cash_flow, revenue)
