from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.daily_price_job import run_daily_price_job
from app.jobs.weekly_financial_job import run_weekly_financial_job
from app.jobs.monthly_valuation_job import run_monthly_valuation_job

def setup_scheduler(scheduler: BackgroundScheduler):
    """
    Registers background jobs with precise Cron timetables.
    """
    
    # Job 1: Daily End-of-Day Price & Drawdown Recalculator
    # Run every Monday through Friday after the US stock market close (e.g., 4:30 PM EST / 16:30)
    scheduler.add_job(
        run_daily_price_job,
        trigger='cron',
        day_of_week='mon-fri',
        hour=16,
        minute=30,
        id='daily_price_and_score_update',
        replace_existing=True
    )

    # Job 2: Weekly Fundamentals & Balance Sheet Update
    # Run every Saturday morning at 2:00 AM (when the market is closed, saving API strain)
    scheduler.add_job(
        run_weekly_financial_job,
        trigger='cron',
        day_of_week='sat',
        hour=2,
        minute=0,
        id='weekly_fundamental_and_analyst_update',
        replace_existing=True
    )

    # Job 3: Daily / Hourly Alert Evaluation trigger
    # Run every Monday through Friday at 5:00 PM EST (after market close and daily score calculations)
    from app.jobs.alert_job import run_alert_job
    scheduler.add_job(
        run_alert_job,
        trigger='cron',
        day_of_week='mon-fri',
        hour=17,
        minute=0,
        id='daily_alert_evaluation_job',
        replace_existing=True
    )
    
    scheduler.add_job(
        run_monthly_valuation_job,
        trigger='cron',
        day=1,
        hour=3,
        minute=0,
        id='monthly_valuation_update',
        replace_existing=True
    )

    print("[Scheduler] Registered background tasks successfully.")

