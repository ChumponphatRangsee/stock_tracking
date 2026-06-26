from datetime import date

from app.normalization.statement_normalizer import StatementNormalizer


def test_statement_normalizer_maps_yahoo_payload():
    raw_statements = [
        {
            "ticker": "AAPL",
            "statement_type": "income_statement",
            "fiscal_year": 2025,
            "fiscal_quarter": None,
            "period_end_date": date(2025, 12, 31),
            "raw_json": {
                "period_type": "annual",
                "line_items": {
                    "Total Revenue": 1000.0,
                    "Gross Profit": 450.0,
                    "Operating Income": 250.0,
                    "Net Income": 200.0,
                    "Diluted Average Shares": 100.0,
                },
            },
        },
        {
            "ticker": "AAPL",
            "statement_type": "balance_sheet",
            "fiscal_year": 2025,
            "fiscal_quarter": None,
            "period_end_date": date(2025, 12, 31),
            "raw_json": {
                "period_type": "annual",
                "line_items": {
                    "Cash And Cash Equivalents": 120.0,
                    "Current Assets": 400.0,
                    "Total Assets": 1000.0,
                    "Current Liabilities": 220.0,
                    "Total Liabilities": 600.0,
                    "Total Debt": 200.0,
                    "Stockholders Equity": 400.0,
                },
            },
        },
        {
            "ticker": "AAPL",
            "statement_type": "cash_flow_statement",
            "fiscal_year": 2025,
            "fiscal_quarter": None,
            "period_end_date": date(2025, 12, 31),
            "raw_json": {
                "period_type": "annual",
                "line_items": {
                    "Operating Cash Flow": 300.0,
                    "Capital Expenditure": -80.0,
                    "Cash Dividends Paid": -20.0,
                    "Repurchase Of Capital Stock": -30.0,
                },
            },
        },
    ]

    normalized = StatementNormalizer().normalize_yahoo_statements(raw_statements)
    income = normalized["income_statements"][0]
    balance = normalized["balance_sheets"][0]
    cash_flow = normalized["cash_flow_statements"][0]

    assert income["revenue"] == 1000.0
    assert balance["invested_capital"] == 480.0
    assert cash_flow["free_cash_flow"] == 220.0
