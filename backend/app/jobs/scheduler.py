from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.update_tasks import (
    update_prices_and_scores_job,
    update_fundamentals_and_analysts_job
)

def setup_scheduler(scheduler: BackgroundScheduler):
    """
    Registers background jobs with precise Cron timetables.
    """
    
    # Job 1: Daily End-of-Day Price & Drawdown Recalculator
    # Run every Monday through Friday after the US stock market close (e.g., 4:30 PM EST / 16:30)
    scheduler.add_job(
        update_prices_and_scores_job,
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
        update_fundamentals_and_analysts_job,
        trigger='cron',
        day_of_week='sat',
        hour=2,
        minute=0,
        id='weekly_fundamental_and_analyst_update',
        replace_existing=True
    )
    
    print("[Scheduler] Registered background tasks successfully.")
