from collections import defaultdict
from typing import Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.normalized_balance_sheet import NormalizedBalanceSheet
from app.models.normalized_income_statement import NormalizedIncomeStatement
from app.models.raw_financial_statement import RawFinancialStatement
from app.models.alert_rule import AlertRule


class StatementRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_raw_statements(self, statements: Iterable[dict]) -> None:
        for statement in statements:
            self.db.add(RawFinancialStatement(**statement))

    def save_normalized_set(self, model, statements: Iterable[dict]) -> None:
        for statement in statements:
            stmt = insert(model).values(**statement).on_conflict_do_nothing()
            self.db.execute(stmt)

    def save_normalized_statements(self, normalized: dict[str, list[dict]]) -> None:
        self.save_normalized_set(NormalizedIncomeStatement, normalized.get("income_statements", []))
        self.save_normalized_set(NormalizedBalanceSheet, normalized.get("balance_sheets", []))
        self.save_normalized_set(NormalizedCashFlowStatement, normalized.get("cash_flow_statements", []))

    def get_latest_statement_bundle(self, ticker: str, period_type: str = "annual") -> dict:
        income = self._latest_rows(NormalizedIncomeStatement, ticker, period_type)
        balance = self._latest_rows(NormalizedBalanceSheet, ticker, period_type)
        cash_flow = self._latest_rows(NormalizedCashFlowStatement, ticker, period_type)
        return {
            "income_statements": income,
            "balance_sheets": balance,
            "cash_flow_statements": cash_flow,
        }

    def list_grouped(self, ticker: str, period_type: str, limit: int) -> dict[str, list]:
        grouped: dict[str, list] = defaultdict(list)
        grouped["income_statements"] = self._latest_rows(NormalizedIncomeStatement, ticker, period_type, limit)
        grouped["balance_sheets"] = self._latest_rows(NormalizedBalanceSheet, ticker, period_type, limit)
        grouped["cash_flow_statements"] = self._latest_rows(NormalizedCashFlowStatement, ticker, period_type, limit)
        return dict(grouped)

    def _latest_rows(self, model, ticker: str, period_type: str, limit: int = 4):
        return (
            self.db.query(model)
            .filter(model.ticker == ticker.upper(), model.period_type == period_type)
            .order_by(model.period_end_date.desc())
            .limit(limit)
            .all()
        )
