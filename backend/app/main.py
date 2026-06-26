from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.api.routes import metrics, refresh, scores, sectors, statements, stocks, valuation, watchlists, alerts
from app.jobs.scheduler import setup_scheduler

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Start the scheduler
    print("Starting APScheduler...")
    setup_scheduler(scheduler)
    scheduler.start()
    
    yield
    
    # Shutdown logic
    print("Shutting down APScheduler...")
    scheduler.shutdown()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Add CORS so React frontend can communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(scores.router, prefix="/api/scores", tags=["Scores"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
app.include_router(valuation.router, prefix="/api/valuation", tags=["Valuation"])
app.include_router(statements.router, prefix="/api/statements", tags=["Statements"])
app.include_router(sectors.router, prefix="/api/sectors", tags=["Sectors"])
app.include_router(watchlists.router, prefix="/api/watchlist", tags=["Watchlist"])
app.include_router(refresh.router, prefix="/api/refresh", tags=["Refresh"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

