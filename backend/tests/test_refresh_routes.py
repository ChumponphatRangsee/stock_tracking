from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes import refresh as refresh_routes
from app.core.database import get_db


class FakePipelineService:
    def __init__(self, db):
        self.db = db

    async def refresh_raw(self, ticker: str):
        return {"ticker": ticker.upper(), "pipeline": "raw", "status": "success", "stages": []}

    async def refresh_full_vi(self, ticker: str):
        return {"ticker": ticker.upper(), "pipeline": "full_vi", "status": "success", "stages": []}


def test_refresh_routes_return_stage_payload(monkeypatch):
    app = FastAPI()
    app.include_router(refresh_routes.router, prefix="/api/refresh")
    app.dependency_overrides[get_db] = lambda: object()
    monkeypatch.setattr(refresh_routes, "ViPipelineService", FakePipelineService)

    client = TestClient(app)

    raw_response = client.post("/api/refresh/AAPL/raw")
    full_response = client.post("/api/refresh/AAPL/full-vi")

    assert raw_response.status_code == 200
    assert raw_response.json()["pipeline"] == "raw"
    assert full_response.status_code == 200
    assert full_response.json()["pipeline"] == "full_vi"
