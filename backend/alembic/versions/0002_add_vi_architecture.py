"""add raw-data-first vi architecture

Revision ID: 0002_add_vi_architecture
Revises: 0001_baseline_current_schema
Create Date: 2026-06-26 00:10:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0002_add_vi_architecture"
down_revision = "0001_baseline_current_schema"
branch_labels = None
depends_on = None


def _has_column(inspector, table_name: str, column_name: str) -> bool:
    return column_name in {column["name"] for column in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "raw_api_responses", "response_json") and not _has_column(inspector, "raw_api_responses", "raw_json"):
        op.add_column("raw_api_responses", sa.Column("raw_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        op.execute("UPDATE raw_api_responses SET raw_json = response_json")

    if _has_column(inspector, "raw_api_responses", "response_hash") and not _has_column(inspector, "raw_api_responses", "data_hash"):
        op.add_column("raw_api_responses", sa.Column("data_hash", sa.String(), nullable=True))
        op.execute("UPDATE raw_api_responses SET data_hash = response_hash")

    if not _has_column(inspector, "raw_api_responses", "data_type"):
        op.add_column("raw_api_responses", sa.Column("data_type", sa.String(), nullable=True))
        op.execute("UPDATE raw_api_responses SET data_type = 'generic' WHERE data_type IS NULL")
        op.alter_column("raw_api_responses", "data_type", nullable=False)

    if not _has_column(inspector, "raw_api_responses", "fetched_at"):
        op.add_column("raw_api_responses", sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now(), nullable=False))

    metric_columns = [
        ("revenue_growth_1y", sa.Numeric()),
        ("revenue_growth_3y_cagr", sa.Numeric()),
        ("ebit_growth_3y_cagr", sa.Numeric()),
        ("fcf_growth_3y_cagr", sa.Numeric()),
        ("roce", sa.Numeric()),
        ("croic", sa.Numeric()),
        ("operating_margin", sa.Numeric()),
        ("fcf_margin", sa.Numeric()),
        ("debt_to_equity", sa.Numeric()),
        ("net_debt_to_ebit", sa.Numeric()),
        ("fcf_yield", sa.Numeric()),
        ("earnings_yield", sa.Numeric()),
        ("ev_ebit", sa.Numeric()),
        ("ev_fcf", sa.Numeric()),
        ("buyback_yield", sa.Numeric()),
        ("share_dilution_pct", sa.Numeric()),
    ]
    for column_name, column_type in metric_columns:
        if not _has_column(inspector, "financial_metrics", column_name):
            op.add_column("financial_metrics", sa.Column(column_name, column_type, nullable=True))

    score_columns = [
        ("trend_score", sa.Numeric()),
        ("risk_score", sa.Numeric()),
        ("margin_of_safety_score", sa.Numeric()),
    ]
    for column_name, column_type in score_columns:
        if not _has_column(inspector, "stock_scores", column_name):
            op.add_column("stock_scores", sa.Column(column_name, column_type, nullable=True))

    op.create_table(
        "raw_financial_statements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(), sa.ForeignKey("stocks.ticker"), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("statement_type", sa.String(), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("fiscal_quarter", sa.Integer(), nullable=True),
        sa.Column("period_end_date", sa.Date(), nullable=False),
        sa.Column("raw_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("accession_number", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_raw_financial_statements_ticker", "raw_financial_statements", ["ticker"])
    op.create_index("ix_raw_financial_statements_period_end_date", "raw_financial_statements", ["period_end_date"])

    op.create_table(
        "normalized_income_statements",
        sa.Column("ticker", sa.String(), sa.ForeignKey("stocks.ticker"), nullable=False),
        sa.Column("period_end_date", sa.Date(), nullable=False),
        sa.Column("period_type", sa.String(), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("fiscal_quarter", sa.Integer(), nullable=True),
        sa.Column("revenue", sa.Numeric(), nullable=True),
        sa.Column("gross_profit", sa.Numeric(), nullable=True),
        sa.Column("operating_income", sa.Numeric(), nullable=True),
        sa.Column("ebit", sa.Numeric(), nullable=True),
        sa.Column("net_income", sa.Numeric(), nullable=True),
        sa.Column("eps_basic", sa.Numeric(), nullable=True),
        sa.Column("eps_diluted", sa.Numeric(), nullable=True),
        sa.Column("shares_basic", sa.Numeric(), nullable=True),
        sa.Column("shares_diluted", sa.Numeric(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("ticker", "period_end_date", "period_type"),
    )

    op.create_table(
        "normalized_balance_sheets",
        sa.Column("ticker", sa.String(), sa.ForeignKey("stocks.ticker"), nullable=False),
        sa.Column("period_end_date", sa.Date(), nullable=False),
        sa.Column("period_type", sa.String(), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("fiscal_quarter", sa.Integer(), nullable=True),
        sa.Column("cash_and_equivalents", sa.Numeric(), nullable=True),
        sa.Column("current_assets", sa.Numeric(), nullable=True),
        sa.Column("total_assets", sa.Numeric(), nullable=True),
        sa.Column("current_liabilities", sa.Numeric(), nullable=True),
        sa.Column("total_liabilities", sa.Numeric(), nullable=True),
        sa.Column("total_debt", sa.Numeric(), nullable=True),
        sa.Column("total_equity", sa.Numeric(), nullable=True),
        sa.Column("invested_capital", sa.Numeric(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("ticker", "period_end_date", "period_type"),
    )

    op.create_table(
        "normalized_cash_flow_statements",
        sa.Column("ticker", sa.String(), sa.ForeignKey("stocks.ticker"), nullable=False),
        sa.Column("period_end_date", sa.Date(), nullable=False),
        sa.Column("period_type", sa.String(), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("fiscal_quarter", sa.Integer(), nullable=True),
        sa.Column("operating_cash_flow", sa.Numeric(), nullable=True),
        sa.Column("capital_expenditure", sa.Numeric(), nullable=True),
        sa.Column("free_cash_flow", sa.Numeric(), nullable=True),
        sa.Column("dividends_paid", sa.Numeric(), nullable=True),
        sa.Column("share_buybacks", sa.Numeric(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("ticker", "period_end_date", "period_type"),
    )

    op.create_table(
        "intrinsic_values",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(), sa.ForeignKey("stocks.ticker"), nullable=False),
        sa.Column("valuation_date", sa.Date(), nullable=False),
        sa.Column("method", sa.String(), nullable=False),
        sa.Column("base_case_value", sa.Numeric(), nullable=True),
        sa.Column("bear_case_value", sa.Numeric(), nullable=True),
        sa.Column("bull_case_value", sa.Numeric(), nullable=True),
        sa.Column("assumptions_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("margin_of_safety_pct", sa.Numeric(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_intrinsic_values_ticker", "intrinsic_values", ["ticker"])
    op.create_index("ix_intrinsic_values_valuation_date", "intrinsic_values", ["valuation_date"])

    op.create_table(
        "macro_indicators",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("indicator_name", sa.String(), nullable=False),
        sa.Column("observation_date", sa.Date(), nullable=False),
        sa.Column("value", sa.Numeric(), nullable=True),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_macro_indicators_indicator_name", "macro_indicators", ["indicator_name"])
    op.create_index("ix_macro_indicators_observation_date", "macro_indicators", ["observation_date"])


def downgrade() -> None:
    op.drop_index("ix_macro_indicators_observation_date", table_name="macro_indicators")
    op.drop_index("ix_macro_indicators_indicator_name", table_name="macro_indicators")
    op.drop_table("macro_indicators")

    op.drop_index("ix_intrinsic_values_valuation_date", table_name="intrinsic_values")
    op.drop_index("ix_intrinsic_values_ticker", table_name="intrinsic_values")
    op.drop_table("intrinsic_values")

    op.drop_table("normalized_cash_flow_statements")
    op.drop_table("normalized_balance_sheets")
    op.drop_table("normalized_income_statements")

    op.drop_index("ix_raw_financial_statements_period_end_date", table_name="raw_financial_statements")
    op.drop_index("ix_raw_financial_statements_ticker", table_name="raw_financial_statements")
    op.drop_table("raw_financial_statements")

    for column_name in ["margin_of_safety_score", "risk_score", "trend_score"]:
        op.drop_column("stock_scores", column_name)

    for column_name in [
        "share_dilution_pct",
        "buyback_yield",
        "ev_fcf",
        "ev_ebit",
        "earnings_yield",
        "fcf_yield",
        "net_debt_to_ebit",
        "debt_to_equity",
        "fcf_margin",
        "operating_margin",
        "croic",
        "roce",
        "fcf_growth_3y_cagr",
        "ebit_growth_3y_cagr",
        "revenue_growth_3y_cagr",
        "revenue_growth_1y",
    ]:
        op.drop_column("financial_metrics", column_name)

    if _has_column(sa.inspect(op.get_bind()), "raw_api_responses", "fetched_at"):
        op.drop_column("raw_api_responses", "fetched_at")
    if _has_column(sa.inspect(op.get_bind()), "raw_api_responses", "data_type"):
        op.drop_column("raw_api_responses", "data_type")
    if _has_column(sa.inspect(op.get_bind()), "raw_api_responses", "data_hash"):
        op.drop_column("raw_api_responses", "data_hash")
    if _has_column(sa.inspect(op.get_bind()), "raw_api_responses", "raw_json"):
        op.drop_column("raw_api_responses", "raw_json")
