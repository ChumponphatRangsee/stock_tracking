from typing import Iterable

from app.normalization.yahoo_mapper import BALANCE_LABELS, CASH_FLOW_LABELS, INCOME_LABELS, pick_value
from app.utils.math_utils import safe_divide


class StatementNormalizer:
    def normalize_yahoo_statements(self, raw_statements: Iterable[dict]) -> dict[str, list[dict]]:
        normalized = {
            "income_statements": [],
            "balance_sheets": [],
            "cash_flow_statements": [],
        }
        for statement in raw_statements:
            statement_type = statement["statement_type"]
            line_items = statement["raw_json"].get("line_items", {})
            base_record = {
                "ticker": statement["ticker"],
                "period_end_date": statement["period_end_date"],
                "period_type": statement["raw_json"].get("period_type", "annual"),
                "fiscal_year": statement["fiscal_year"],
                "fiscal_quarter": statement.get("fiscal_quarter"),
            }

            if statement_type == "income_statement":
                record = {
                    **base_record,
                    **{field: pick_value(line_items, labels) for field, labels in INCOME_LABELS.items()},
                }
                normalized["income_statements"].append(record)
            elif statement_type == "balance_sheet":
                total_debt = pick_value(line_items, BALANCE_LABELS["total_debt"])
                total_equity = pick_value(line_items, BALANCE_LABELS["total_equity"])
                cash = pick_value(line_items, BALANCE_LABELS["cash_and_equivalents"])
                record = {
                    **base_record,
                    **{field: pick_value(line_items, labels) for field, labels in BALANCE_LABELS.items()},
                    "invested_capital": (total_debt or 0.0) + (total_equity or 0.0) - (cash or 0.0),
                }
                normalized["balance_sheets"].append(record)
            elif statement_type == "cash_flow_statement":
                operating_cash_flow = pick_value(line_items, CASH_FLOW_LABELS["operating_cash_flow"])
                capital_expenditure = pick_value(line_items, CASH_FLOW_LABELS["capital_expenditure"])
                record = {
                    **base_record,
                    **{field: pick_value(line_items, labels) for field, labels in CASH_FLOW_LABELS.items()},
                    "free_cash_flow": (operating_cash_flow or 0.0) - abs(capital_expenditure or 0.0),
                }
                normalized["cash_flow_statements"].append(record)

        return normalized

    def summarize_statement_health(self, normalized: dict[str, list[dict]]) -> dict[str, float]:
        income = normalized.get("income_statements", [])
        cash_flow = normalized.get("cash_flow_statements", [])
        if not income or not cash_flow:
            return {}
        latest_income = income[0]
        latest_cash = cash_flow[0]
        return {
            "fcf_margin": safe_divide(latest_cash.get("free_cash_flow"), latest_income.get("revenue")),
        }
