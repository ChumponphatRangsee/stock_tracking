from datetime import date

from sqlalchemy.orm import Session

from app.models.macro_indicator import MacroIndicator


class MacroIngestion:
    def __init__(self, db: Session):
        self.db = db

    def store_observations(self, indicator_name: str, observations: list[dict], source: str, metadata: dict | None = None) -> int:
        inserted = 0
        for observation in observations:
            value = observation.get("value")
            if value in (None, ".", ""):
                continue
            self.db.add(
                MacroIndicator(
                    indicator_name=indicator_name,
                    observation_date=date.fromisoformat(observation["date"]),
                    value=float(value),
                    source=source,
                    metadata_json=metadata or {},
                )
            )
            inserted += 1
        return inserted
