from sqlalchemy.orm import Session

from app.normalization.statement_normalizer import StatementNormalizer
from app.repositories.statement_repository import StatementRepository


class FinancialStatementIngestion:
    def __init__(self, db: Session):
        self.db = db
        self.repository = StatementRepository(db)
        self.normalizer = StatementNormalizer()

    def store_raw(self, raw_statements: list[dict]) -> None:
        self.repository.add_raw_statements(raw_statements)

    def normalize_and_store(self, raw_statements: list[dict]) -> dict[str, list[dict]]:
        normalized = self.normalizer.normalize_yahoo_statements(raw_statements)
        self.repository.save_normalized_statements(normalized)
        return normalized
