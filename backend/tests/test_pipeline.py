import asyncio

from app.services.vi_pipeline_service import ViPipelineService


class FakeDB:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


class PartialSuccessPipeline(ViPipelineService):
    def __init__(self):
        self.db = FakeDB()

    async def _fetch_market_data(self, ticker, context):
        context["quote"] = {"close_price": 100.0}
        return {"records": 1}

    async def _fetch_financial_statements(self, ticker, context):
        raise ValueError("statement fetch failed")

    async def _fetch_analyst_data(self, ticker, context):
        return {"records": 1}

    async def _fetch_sec_data(self, ticker, context):
        return {"records": 0}

    async def _fetch_macro_data(self, context):
        return {"records": 0}


def test_pipeline_returns_partial_success_without_crashing():
    result = asyncio.run(PartialSuccessPipeline().refresh_raw("AAPL"))
    assert result["status"] == "partial_success"
    assert any(stage["name"] == "financial_statements" and stage["status"] == "failed" for stage in result["stages"])
