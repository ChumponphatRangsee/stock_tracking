from app.utils.math_utils import safe_divide


def calculate_earnings_yield(net_income, market_cap) -> float:
    return safe_divide(net_income, market_cap)


def calculate_fcf_yield(free_cash_flow, market_cap) -> float:
    return safe_divide(free_cash_flow, market_cap)


def calculate_ev_ebit(enterprise_value, ebit) -> float:
    return safe_divide(enterprise_value, ebit)


def calculate_ev_fcf(enterprise_value, free_cash_flow) -> float:
    return safe_divide(enterprise_value, free_cash_flow)


def calculate_buyback_yield(share_buybacks, market_cap) -> float:
    return safe_divide(abs(float(share_buybacks or 0.0)), market_cap)
