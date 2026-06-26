from app.utils.math_utils import safe_divide


def calculate_gross_margin(gross_profit, revenue) -> float:
    return safe_divide(gross_profit, revenue)


def calculate_operating_margin(operating_income, revenue) -> float:
    return safe_divide(operating_income, revenue)


def calculate_net_margin(net_income, revenue) -> float:
    return safe_divide(net_income, revenue)
