from app.normalization.unit_converter import to_float


SEC_FACT_LABELS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
    "operating_income": ["OperatingIncomeLoss"],
    "cash_and_equivalents": ["CashAndCashEquivalentsAtCarryingValue"],
    "total_assets": ["Assets"],
    "total_liabilities": ["Liabilities"],
}


def extract_sec_fact(facts: dict, keys: list[str]):
    for key in keys:
        value = facts.get(key)
        if value is not None:
            return to_float(value)
    return None
