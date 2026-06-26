from app.utils.math_utils import safe_divide


def calculate_roic(nopat, invested_capital) -> float:
    return safe_divide(nopat, invested_capital)


def calculate_roe(net_income, total_equity) -> float:
    return safe_divide(net_income, total_equity)


def calculate_roce(ebit, capital_employed) -> float:
    return safe_divide(ebit, capital_employed)


def calculate_croic(free_cash_flow, invested_capital) -> float:
    return safe_divide(free_cash_flow, invested_capital)
