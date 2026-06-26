from app.scoring.opportunity_score import calculate_opportunity_score
from app.valuation.dcf import calculate_dcf
from app.valuation.margin_of_safety import calculate_margin_of_safety


def test_dcf_valuation_returns_positive_per_share_value():
    result = calculate_dcf(
        starting_fcf=100.0,
        growth_years=5,
        growth_rate=0.08,
        terminal_growth_rate=0.025,
        discount_rate=0.10,
        shares_outstanding=50.0,
        net_cash_or_debt=25.0,
    )
    assert result["per_share_value"] > 0


def test_margin_of_safety():
    assert round(calculate_margin_of_safety(60.0, 100.0), 4) == 0.4


def test_updated_opportunity_score_weighting():
    result = calculate_opportunity_score(
        quality_score=80.0,
        valuation_score=70.0,
        margin_of_safety_score=60.0,
        trend_score=50.0,
        risk_score=20.0,
        analyst_score=40.0,
    )
    assert round(result, 2) == 69.5
