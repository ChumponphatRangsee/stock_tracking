from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.alert_rule import AlertRule
from app.models.stock import Stock
from pydantic import BaseModel, ConfigDict

router = APIRouter()

class AlertRuleCreate(BaseModel):
    ticker: str
    metric: str
    condition: str
    value_threshold: float

class AlertRuleResponse(BaseModel):
    id: int
    ticker: str
    metric: str
    condition: str
    value_threshold: float
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.get("/", response_model=List[AlertRuleResponse])
def get_alerts(db: Session = Depends(get_db)):
    """Retrieve all alert rules."""
    return db.query(AlertRule).order_by(AlertRule.created_at.desc()).all()

@router.post("/", response_model=AlertRuleResponse)
def create_alert(alert: AlertRuleCreate, db: Session = Depends(get_db)):
    """Creates a new alert rule."""
    ticker_upper = alert.ticker.upper()
    
    # Check if stock exists
    stock = db.query(Stock).filter(Stock.ticker == ticker_upper).first()
    if not stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock {ticker_upper} must exist in the monitored universe before setting alerts."
        )
        
    db_alert = AlertRule(
        ticker=ticker_upper,
        metric=alert.metric,
        condition=alert.condition,
        value_threshold=alert.value_threshold,
        is_active=True
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.patch("/{alert_id}/toggle", response_model=AlertRuleResponse)
def toggle_alert(alert_id: int, db: Session = Depends(get_db)):
    """Enables or disables an alert rule."""
    alert = db.query(AlertRule).filter(AlertRule.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert rule not found")
        
    alert.is_active = not alert.is_active
    db.commit()
    db.refresh(alert)
    return alert

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Removes an alert rule."""
    alert = db.query(AlertRule).filter(AlertRule.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert rule not found")
        
    db.delete(alert)
    db.commit()
    return {"message": f"Successfully deleted alert rule {alert_id}"}
