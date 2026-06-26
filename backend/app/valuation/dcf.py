from app.utils.math_utils import safe_divide


def calculate_dcf(
    starting_fcf: float,
    growth_years: int,
    growth_rate: float,
    terminal_growth_rate: float,
    discount_rate: float,
    shares_outstanding: float,
    net_cash_or_debt: float,
) -> dict:
    projected_cash_flows = []
    current_fcf = float(starting_fcf or 0.0)

    for year in range(1, growth_years + 1):
        current_fcf *= 1 + growth_rate
        projected_cash_flows.append(current_fcf / ((1 + discount_rate) ** year))

    terminal_fcf = current_fcf * (1 + terminal_growth_rate)
    terminal_value = safe_divide(terminal_fcf, discount_rate - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** growth_years) if terminal_value else 0.0
    enterprise_value = sum(projected_cash_flows) + discounted_terminal_value
    equity_value = enterprise_value + float(net_cash_or_debt or 0.0)
    per_share_value = safe_divide(equity_value, shares_outstanding)

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share_value": per_share_value,
    }
