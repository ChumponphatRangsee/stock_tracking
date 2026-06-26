from app.normalization.unit_converter import to_float


INCOME_LABELS = {
    "revenue": ["Total Revenue", "Operating Revenue"],
    "gross_profit": ["Gross Profit"],
    "operating_income": ["Operating Income"],
    "ebit": ["EBIT", "Operating Income"],
    "net_income": ["Net Income", "Net Income Common Stockholders"],
    "eps_basic": ["Basic EPS"],
    "eps_diluted": ["Diluted EPS"],
    "shares_basic": ["Basic Average Shares"],
    "shares_diluted": ["Diluted Average Shares"],
}

BALANCE_LABELS = {
    "cash_and_equivalents": ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"],
    "current_assets": ["Current Assets", "Total Current Assets"],
    "total_assets": ["Total Assets"],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"],
    "total_liabilities": ["Total Liabilities Net Minority Interest", "Total Liabilities"],
    "total_debt": ["Total Debt"],
    "total_equity": ["Stockholders Equity", "Total Stockholders Equity", "Common Stock Equity"],
}

CASH_FLOW_LABELS = {
    "operating_cash_flow": ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"],
    "capital_expenditure": ["Capital Expenditure", "Capital Expenditure Reported"],
    "dividends_paid": ["Cash Dividends Paid", "Common Stock Dividend Paid"],
    "share_buybacks": ["Repurchase Of Capital Stock", "Common Stock Payments"],
}


def pick_value(line_items: dict, labels: list[str]):
    for label in labels:
        if label in line_items:
            return to_float(line_items[label])
    return None
