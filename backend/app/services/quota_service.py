from datetime import date
from sqlalchemy.orm import Session
from app.models.api_usage_log import ApiUsageLog

# Free Tier Limits
PROVIDER_LIMITS = {
    "FMP": 250,
    "Finnhub": 300,
    "SEC": 600,
    "FRED": 300,
}

class QuotaService:
    @staticmethod
    def can_make_request(db: Session, provider: str) -> bool:
        """Check if we have enough API quota left for today."""
        today = date.today()
        log = db.query(ApiUsageLog).filter(
            ApiUsageLog.provider == provider,
            ApiUsageLog.usage_date == today
        ).first()

        if not log:
            return True  # No requests made today yet

        limit = PROVIDER_LIMITS.get(provider, 100)
        return log.request_count < limit

    @staticmethod
    def increment_quota(db: Session, provider: str):
        """Increment the daily usage count for a provider."""
        today = date.today()
        log = db.query(ApiUsageLog).filter(
            ApiUsageLog.provider == provider,
            ApiUsageLog.usage_date == today
        ).first()

        if log:
            log.request_count += 1
        else:
            log = ApiUsageLog(provider=provider, usage_date=today, request_count=1)
            db.add(log)
        
        db.commit()
