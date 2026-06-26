from app.valuation.dcf import calculate_dcf


def calculate_owner_earnings_value(
    owner_earnings: float,
    shares_outstanding: float,
    net_cash_or_debt: float,
    growth_rate: float = 0.05,
    terminal_growth_rate: float = 0.025,
    discount_rate: float = 0.10,
    growth_years: int = 10,
) -> dict:
    return calculate_dcf(
        starting_fcf=owner_earnings,
        growth_years=growth_years,
        growth_rate=growth_rate,
        terminal_growth_rate=terminal_growth_rate,
        discount_rate=discount_rate,
        shares_outstanding=shares_outstanding,
        net_cash_or_debt=net_cash_or_debt,
    )
