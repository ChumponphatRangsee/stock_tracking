from app.utils.math_utils import safe_divide


def calculate_debt_to_equity(total_debt, total_equity) -> float:
    return safe_divide(total_debt, total_equity)


def calculate_current_ratio(current_assets, current_liabilities) -> float:
    return safe_divide(current_assets, current_liabilities)


def calculate_net_debt_to_ebit(total_debt, cash_and_equivalents, ebit) -> float:
    net_debt = float(total_debt or 0.0) - float(cash_and_equivalents or 0.0)
    return safe_divide(net_debt, ebit)
