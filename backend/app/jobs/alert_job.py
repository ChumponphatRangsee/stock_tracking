from datetime import date
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.alert_rule import AlertRule
from app.models.stock_price import StockPrice
from app.models.financial_metric import FinancialMetric
from app.models.intrinsic_value import IntrinsicValue

def run_alert_job():
    """
    Evaluates active alert rules against the latest market prices and calculated metrics/valuations.
    """
    print("[Scheduler] Running active alert rule evaluations...")
    db = SessionLocal()
    try:
        active_alerts = db.query(AlertRule).filter(AlertRule.is_active == True).all()
        if not active_alerts:
            print("[Scheduler] No active alert rules configured.")
            return

        for alert in active_alerts:
            try:
                # 1. Fetch current price
                latest_price_row = db.query(StockPrice).filter(
                    StockPrice.ticker == alert.ticker
                ).order_by(StockPrice.price_date.desc()).first()
                current_price = float(latest_price_row.close_price) if latest_price_row and latest_price_row.close_price is not None else None

                # 2. Fetch latest metric
                latest_metric_row = db.query(FinancialMetric).filter(
                    FinancialMetric.ticker == alert.ticker
                ).order_by(FinancialMetric.snapshot_date.desc()).first()

                # 3. Fetch latest DCF / margin of safety
                latest_val_row = db.query(IntrinsicValue).filter(
                    IntrinsicValue.ticker == alert.ticker,
                    IntrinsicValue.method == 'dcf'
                ).order_by(IntrinsicValue.valuation_date.desc()).first()

                # Extract metric value based on configuration
                actual_val = None
                if alert.metric == 'price':
                    actual_val = current_price
                elif alert.metric == 'pe_ratio':
                    actual_val = float(latest_metric_row.pe_ratio or latest_metric_row.forward_pe or 0) if latest_metric_row else None
                elif alert.metric == 'margin_of_safety_pct':
                    actual_val = float(latest_val_row.margin_of_safety_pct) if latest_val_row and latest_val_row.margin_of_safety_pct is not None else None

                if actual_val is None:
                    continue

                # Check condition
                triggered = False
                threshold = float(alert.value_threshold)
                if alert.condition == 'less_than':
                    triggered = actual_val < threshold
                elif alert.condition == 'greater_than':
                    triggered = actual_val > threshold

                if triggered:
                    print(f"[ALERT TRIGGERED] Ticker: {alert.ticker} | Metric: {alert.metric} | Value: {actual_val} | Target: {threshold}")
                    alert.last_triggered_at = date.today()
                    # Optional: Deactivate rule so it doesn't spam alert fires on every cron cycle
                    alert.is_active = False

            except Exception as item_err:
                print(f"[Scheduler] Error evaluating alert ID {alert.id} for {alert.ticker}: {item_err}")
        db.commit()
    except Exception as e:
        print(f"[Scheduler] Alert evaluation job failed: {e}")
    finally:
        db.close()

