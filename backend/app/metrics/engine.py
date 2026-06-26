from datetime import date

from app.metrics.balance_sheet import calculate_current_ratio, calculate_debt_to_equity, calculate_net_debt_to_ebit
from app.metrics.capital_allocation import calculate_croic, calculate_roe, calculate_roce, calculate_roic
from app.metrics.cash_flow import calculate_fcf_margin
from app.metrics.growth import calculate_growth, calculate_three_year_cagr
from app.metrics.profitability import calculate_gross_margin, calculate_net_margin, calculate_operating_margin
from app.metrics.valuation import (
    calculate_buyback_yield,
    calculate_earnings_yield,
    calculate_ev_ebit,
    calculate_ev_fcf,
    calculate_fcf_yield,
)
from app.utils.math_utils import safe_divide


class MetricsEngine:
    def calculate(self, ticker: str, statement_bundle: dict, supplemental: dict, latest_price) -> dict:
        income_statements = statement_bundle.get("income_statements", [])
        balance_sheets = statement_bundle.get("balance_sheets", [])
        cash_flow_statements = statement_bundle.get("cash_flow_statements", [])
        if not income_statements or not balance_sheets or not cash_flow_statements:
            raise ValueError("Normalized statement bundle is incomplete")

        latest_income = income_statements[0]
        latest_balance = balance_sheets[0]
        latest_cash_flow = cash_flow_statements[0]
        prev_income = income_statements[1] if len(income_statements) > 1 else None
        prev_cash_flow = cash_flow_statements[1] if len(cash_flow_statements) > 1 else None
        prior_three_income = income_statements[3] if len(income_statements) > 3 else None
        prior_three_cash = cash_flow_statements[3] if len(cash_flow_statements) > 3 else None

        revenue = float(latest_income.revenue or 0.0)
        gross_profit = float(latest_income.gross_profit or 0.0)
        operating_income = float(latest_income.operating_income or 0.0)
        ebit = float(latest_income.ebit or 0.0)
        net_income = float(latest_income.net_income or 0.0)
        total_equity = float(latest_balance.total_equity or 0.0)
        total_debt = float(latest_balance.total_debt or 0.0)
        current_assets = float(latest_balance.current_assets or 0.0)
        current_liabilities = float(latest_balance.current_liabilities or 0.0)
        cash = float(latest_balance.cash_and_equivalents or 0.0)
        invested_capital = float(latest_balance.invested_capital or 0.0)
        total_assets = float(latest_balance.total_assets or 0.0)
        free_cash_flow = float(latest_cash_flow.free_cash_flow or 0.0)
        share_buybacks = float(latest_cash_flow.share_buybacks or 0.0)
        market_cap = float(getattr(latest_price, "close_price", 0.0) or 0.0) * float(latest_income.shares_diluted or latest_income.shares_basic or 0.0)

        nopat = ebit * 0.79
        enterprise_value = market_cap + total_debt - cash
        capital_employed = total_assets - current_liabilities

        revenue_growth_1y = calculate_growth(revenue, getattr(prev_income, "revenue", None))
        ebit_growth_1y = calculate_growth(ebit, getattr(prev_income, "ebit", None))
        fcf_growth_1y = calculate_growth(free_cash_flow, getattr(prev_cash_flow, "free_cash_flow", None))
        share_dilution_pct = calculate_growth(
            float(latest_income.shares_diluted or latest_income.shares_basic or 0.0),
            getattr(prior_three_income, "shares_diluted", None) or getattr(prior_three_income, "shares_basic", None),
        )

        return {
            "ticker": ticker,
            "snapshot_date": date.today(),
            "source": "internal_vi",
            "forward_pe": supplemental.get("forward_pe"),
            "pe_ratio": supplemental.get("pe_ratio"),
            "ps_ratio": supplemental.get("ps_ratio"),
            "peg_ratio": supplemental.get("peg_ratio"),
            "revenue_growth": revenue_growth_1y,
            "revenue_growth_1y": revenue_growth_1y,
            "revenue_growth_3y_cagr": calculate_three_year_cagr(revenue, getattr(prior_three_income, "revenue", None)),
            "eps_growth": supplemental.get("eps_growth"),
            "ebit_growth": ebit_growth_1y,
            "ebit_growth_3y_cagr": calculate_three_year_cagr(ebit, getattr(prior_three_income, "ebit", None)),
            "fcf_growth_3y_cagr": calculate_three_year_cagr(free_cash_flow, getattr(prior_three_cash, "free_cash_flow", None)),
            "gross_margin": calculate_gross_margin(gross_profit, revenue),
            "ebit_margin": calculate_operating_margin(operating_income, revenue),
            "operating_margin": calculate_operating_margin(operating_income, revenue),
            "net_margin": calculate_net_margin(net_income, revenue),
            "fcf_margin": calculate_fcf_margin(free_cash_flow, revenue),
            "roe": calculate_roe(net_income, total_equity),
            "roic": calculate_roic(nopat, invested_capital),
            "roce": calculate_roce(ebit, capital_employed),
            "croic": calculate_croic(free_cash_flow, invested_capital),
            "debt_equity": calculate_debt_to_equity(total_debt, total_equity),
            "debt_to_equity": calculate_debt_to_equity(total_debt, total_equity),
            "net_debt_to_ebit": calculate_net_debt_to_ebit(total_debt, cash, ebit),
            "current_ratio": calculate_current_ratio(current_assets, current_liabilities),
            "fcf_yield": calculate_fcf_yield(free_cash_flow, market_cap),
            "earnings_yield": calculate_earnings_yield(net_income, market_cap),
            "ev_ebit": calculate_ev_ebit(enterprise_value, ebit),
            "ev_fcf": calculate_ev_fcf(enterprise_value, free_cash_flow),
            "buyback_yield": calculate_buyback_yield(share_buybacks, market_cap),
            "share_dilution_pct": share_dilution_pct,
            "implied_market_cap": market_cap,
            "share_count": float(latest_income.shares_diluted or latest_income.shares_basic or 0.0),
            "fcf_growth_1y": fcf_growth_1y,
            "cash_value": cash,
            "net_income_value": net_income,
            "ebit_value": ebit,
            "free_cash_flow_value": free_cash_flow,
            "invested_capital_value": invested_capital,
            "total_debt_value": total_debt,
        }
