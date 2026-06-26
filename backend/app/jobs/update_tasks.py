from app.jobs.daily_price_job import run_daily_price_job
from app.jobs.weekly_financial_job import run_weekly_financial_job


def update_prices_and_scores_job():
    run_daily_price_job()


def update_fundamentals_and_analysts_job():
    run_weekly_financial_job()
