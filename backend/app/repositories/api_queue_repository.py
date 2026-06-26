from typing import Optional
from sqlalchemy.orm import Session
from app.models.api_request_queue import ApiRequestQueue

class ApiQueueRepository:
    @staticmethod
    def add_to_queue(
        db: Session, 
        provider: str, 
        endpoint: str, 
        ticker: str, 
        priority: int = 100
    ) -> ApiRequestQueue:
        """Adds a new API request task to the queue."""
        task = ApiRequestQueue(
            provider=provider,
            endpoint=endpoint,
            ticker=ticker,
            priority=priority,
            status="PENDING"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_next_pending_task(db: Session, provider: str) -> Optional[ApiRequestQueue]:
        """Gets the highest priority task that is ready to execute."""
        return db.query(ApiRequestQueue).filter(
            ApiRequestQueue.status == "PENDING",
            ApiRequestQueue.provider == provider,
            # We would also check execute_after here if we implement backoff delays
        ).order_by(ApiRequestQueue.priority.asc()).first()

    @staticmethod
    def mark_task_completed(db: Session, task: ApiRequestQueue):
        task.status = "COMPLETED"
        db.commit()

    @staticmethod
    def mark_task_failed(db: Session, task: ApiRequestQueue, error: str):
        task.status = "FAILED"
        task.error_message = error
        task.retry_count += 1
        db.commit()
