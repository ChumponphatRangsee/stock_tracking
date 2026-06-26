import inspect
from datetime import date, datetime, timezone
from typing import Any, Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.metrics.engine import MetricsEngine
from app.models.analyst_data import AnalystData
from app.models.macro_indicator import MacroIndicator
from app.models.stock_price import StockPrice
from app.normalization.statement_normalizer import StatementNormalizer
from app.providers.provider_factory import ProviderFactory
from app.repositories.metric_repository import MetricRepository
from app.repositories.raw_data_repository import RawDataRepository
from app.repositories.score_repository import ScoreRepository
from app.repositories.statement_repository import StatementRepository
from app.repositories.stock_repository import StockRepository
from app.repositories.valuation_repository import ValuationRepository
from app.services.stock_service import StockService
from app.valuation.dcf import calculate_dcf
from app.valuation.margin_of_safety import calculate_margin_of_safety
from app.valuation.owner_earnings import calculate_owner_earnings_value


class ViPipelineService:
    def __init__(
        self,
        db: Session,
        yahoo_provider=None,
        analyst_provider=None,
        sec_provider=None,
        fred_provider=None,
        normalizer: Optional[StatementNormalizer] = None,
        metrics_engine: Optional[MetricsEngine] = None,
    ):
        self.db = db
        self.yahoo_provider = yahoo_provider or ProviderFactory.get_financial_data_provider()
        self.analyst_provider = analyst_provider or ProviderFactory.get_analyst_data_provider(db)
        self.sec_provider = sec_provider or ProviderFactory.get_sec_provider(db)
        self.fred_provider = fred_provider or ProviderFactory.get_fred_provider(db)
        self.normalizer = normalizer or StatementNormalizer()
        self.metrics_engine = metrics_engine or MetricsEngine()
        self.stock_repository = StockRepository(db)
        self.raw_repository = RawDataRepository(db)
        self.statement_repository = StatementRepository(db)
        self.metric_repository = MetricRepository(db)
        self.valuation_repository = ValuationRepository(db)
        self.score_repository = ScoreRepository(db)

    async def refresh_raw(self, ticker: str) -> dict[str, Any]:
        return await self._run_pipeline(ticker.upper(), full_vi=False)

    async def refresh_full_vi(self, ticker: str) -> dict[str, Any]:
        return await self._run_pipeline(ticker.upper(), full_vi=True)

    async def _run_pipeline(self, ticker: str, full_vi: bool) -> dict[str, Any]:
        result: dict[str, Any] = {
            "ticker": ticker,
            "pipeline": "full_vi" if full_vi else "raw",
            "status": "success",
            "stages": [],
        }
        raw_context: dict[str, Any] = {}

        await self._stage(result, "market_data", lambda: self._fetch_market_data(ticker, raw_context))
        await self._stage(result, "financial_statements", lambda: self._fetch_financial_statements(ticker, raw_context))
        await self._stage(result, "analyst_data", lambda: self._fetch_analyst_data(ticker, raw_context))
        await self._stage(result, "sec_edgar", lambda: self._fetch_sec_data(ticker, raw_context))
        await self._stage(result, "macro_data", lambda: self._fetch_macro_data(raw_context))

        if full_vi:
            await self._stage(result, "normalize_statements", lambda: self._normalize_statements(raw_context))
            await self._stage(result, "metrics", lambda: self._calculate_metrics(ticker, raw_context))
            await self._stage(result, "valuation", lambda: self._calculate_valuations(ticker, raw_context))
            await self._stage(result, "scores", lambda: self._calculate_scores(ticker))

        self.db.commit()
        return result

    async def _stage(self, result: dict, name: str, func) -> None:
        started_at = datetime.now(timezone.utc).isoformat()
        stage_result = {"name": name, "status": "success", "started_at": started_at}
        try:
            payload = func()
            if inspect.isawaitable(payload):
                payload = await payload
            if isinstance(payload, dict):
                stage_result.update(payload)
            self.db.commit()
        except Exception as exc:
            self.db.rollback()
            stage_result["status"] = "failed"
            stage_result["error"] = str(exc)
            result["status"] = "partial_success"
        stage_result["finished_at"] = datetime.now(timezone.utc).isoformat()
        result["stages"].append(stage_result)

    def _save_price_snapshot(self, ticker: str, quote_data: dict) -> None:
        stmt = insert(StockPrice).values(
            ticker=ticker,
            price_date=date.today(),
            **quote_data,
        ).on_conflict_do_nothing()
        self.db.execute(stmt)

    def _save_analyst_snapshot(self, ticker: str, analyst_data: dict) -> None:
        stmt = insert(AnalystData).values(
            ticker=ticker,
            snapshot_date=date.today(),
            source=analyst_data.pop("source", "Finnhub/Yahoo"),
            **analyst_data,
        ).on_conflict_do_nothing()
        self.db.execute(stmt)

    async def _fetch_market_data(self, ticker: str, context: dict) -> dict:
        profile = await self.yahoo_provider.get_company_profile(ticker)
        quote = await self.yahoo_provider.get_quote(ticker)
        raw_company_payload = await self.yahoo_provider.get_raw_company_payload(ticker)
        supplemental = await self.yahoo_provider.get_financial_metrics(ticker) or {}
        self.raw_repository.save_response("Yahoo", "company/info", ticker, "company_info", raw_company_payload)
        self.raw_repository.save_response("Yahoo", "company/supplemental", ticker, "supplemental_metrics", supplemental)

        if not profile:
            raise ValueError("Yahoo profile fetch returned no data")

        self.stock_repository.upsert(ticker, profile)
        if quote:
            self._save_price_snapshot(ticker, quote)

        context["profile"] = profile
        context["quote"] = quote
        context["supplemental"] = supplemental
        return {"records": int(bool(profile)) + int(bool(quote))}

    async def _fetch_financial_statements(self, ticker: str, context: dict) -> dict:
        raw_statements = await self.yahoo_provider.get_raw_financial_statements(ticker)
        if not raw_statements:
            raise ValueError("Yahoo statements fetch returned no data")
        self.statement_repository.add_raw_statements(raw_statements)
        context["raw_statements"] = raw_statements
        return {"records": len(raw_statements)}

    async def _fetch_analyst_data(self, ticker: str, context: dict) -> dict:
        analyst = await self.analyst_provider.get_analyst_data(ticker) or {}
        supplemental = context.get("supplemental", {})
        merged = dict(analyst)
        for field in ("target_price_avg", "target_price_high", "target_price_low"):
            if supplemental.get(field) is not None:
                merged[field] = supplemental.get(field)

        current_price = (context.get("quote") or {}).get("close_price")
        average_target = merged.get("target_price_avg")
        if current_price and average_target:
            merged["target_upside_pct"] = ((average_target - current_price) / current_price)
        merged["source"] = "Finnhub/Yahoo"
        if merged:
            self._save_analyst_snapshot(ticker, merged)
        context["analyst"] = merged
        return {"records": int(bool(merged))}

    async def _fetch_sec_data(self, ticker: str, context: dict) -> dict:
        facts = await self.sec_provider.get_company_facts(ticker)
        context["sec_company_facts"] = facts
        return {"records": int(bool(facts))}

    async def _fetch_macro_data(self, context: dict) -> dict:
        macro_payloads = await self.fred_provider.fetch_all()
        record_count = 0
        for indicator_name, observations in macro_payloads.items():
            for observation in observations[-12:]:
                if observation.get("value") in (None, ".", ""):
                    continue
                self.db.add(
                    MacroIndicator(
                        indicator_name=indicator_name,
                        observation_date=date.fromisoformat(observation["date"]),
                        value=float(observation["value"]),
                        source="FRED",
                        metadata_json={"series_id": self.fred_provider.series[indicator_name]},
                    )
                )
                record_count += 1
        context["macro_payloads"] = macro_payloads
        return {"records": record_count}

    def _normalize_statements(self, context: dict) -> dict:
        normalized = self.normalizer.normalize_yahoo_statements(context.get("raw_statements", []))
        if not normalized["income_statements"]:
            raise ValueError("No normalized income statements were produced")
        self.statement_repository.save_normalized_statements(normalized)
        self.db.commit()
        ticker = normalized["income_statements"][0]["ticker"]
        context["normalized"] = self.statement_repository.get_latest_statement_bundle(ticker)
        return {
            "records": (
                len(normalized["income_statements"])
                + len(normalized["balance_sheets"])
                + len(normalized["cash_flow_statements"])
            )
        }

    def _calculate_metrics(self, ticker: str, context: dict) -> dict:
        latest_price = (
            self.db.query(StockPrice)
            .filter(StockPrice.ticker == ticker)
            .order_by(StockPrice.price_date.desc())
            .first()
        )
        metrics_payload = self.metrics_engine.calculate(
            ticker,
            context["normalized"],
            context.get("supplemental", {}),
            latest_price,
        )
        context["metrics_payload"] = metrics_payload
        self.metric_repository.save_snapshot(
            {key: value for key, value in metrics_payload.items() if key in self._metric_columns()}
        )
        self.db.commit()
        return {"records": 1}

    def _calculate_valuations(self, ticker: str, context: dict) -> dict:
        latest_price = (
            self.db.query(StockPrice)
            .filter(StockPrice.ticker == ticker)
            .order_by(StockPrice.price_date.desc())
            .first()
        )
        current_price = float(getattr(latest_price, "close_price", 0.0) or 0.0)
        metrics_payload = context["metrics_payload"]
        shares_outstanding = metrics_payload["share_count"] or 1.0
        net_cash_or_debt = metrics_payload["cash_value"] - metrics_payload["total_debt_value"]
        starting_fcf = metrics_payload["free_cash_flow_value"]

        dcf_assumptions = {
            "starting_fcf": starting_fcf,
            "growth_years": 10,
            "growth_rate": max(0.02, metrics_payload["revenue_growth_3y_cagr"] or 0.04),
            "terminal_growth_rate": 0.025,
            "discount_rate": 0.10,
            "shares_outstanding": shares_outstanding,
            "net_cash_or_debt": net_cash_or_debt,
        }
        dcf_value = calculate_dcf(**dcf_assumptions)
        owner_earnings_value = calculate_owner_earnings_value(
            owner_earnings=starting_fcf,
            shares_outstanding=shares_outstanding,
            net_cash_or_debt=net_cash_or_debt,
            growth_rate=0.05,
            terminal_growth_rate=0.025,
            discount_rate=0.10,
            growth_years=10,
        )

        valuations = []
        for method, payload in (
            ("dcf", dcf_value),
            ("owner_earnings", owner_earnings_value),
        ):
            base_value = float(payload["per_share_value"] or 0.0)
            margin = calculate_margin_of_safety(current_price, base_value)
            valuations.append(
                {
                    "ticker": ticker,
                    "valuation_date": date.today(),
                    "method": method,
                    "base_case_value": base_value,
                    "bear_case_value": base_value * 0.8,
                    "bull_case_value": base_value * 1.2,
                    "assumptions_json": dcf_assumptions if method == "dcf" else {
                        "owner_earnings": starting_fcf,
                        "shares_outstanding": shares_outstanding,
                        "net_cash_or_debt": net_cash_or_debt,
                    },
                    "margin_of_safety_pct": margin,
                }
            )
        self.valuation_repository.add_all(valuations)
        context["valuations"] = valuations
        return {"records": len(valuations)}

    def _calculate_scores(self, ticker: str) -> dict:
        StockService(self.db).calculate_and_save_scores(ticker)
        return {"records": 1}

    @staticmethod
    def _metric_columns() -> set[str]:
        return {
            "ticker",
            "snapshot_date",
            "forward_pe",
            "pe_ratio",
            "ps_ratio",
            "peg_ratio",
            "revenue_growth",
            "revenue_growth_1y",
            "revenue_growth_3y_cagr",
            "eps_growth",
            "ebit_growth",
            "ebit_growth_3y_cagr",
            "fcf_growth_3y_cagr",
            "gross_margin",
            "ebit_margin",
            "operating_margin",
            "net_margin",
            "fcf_margin",
            "roe",
            "roic",
            "roce",
            "croic",
            "debt_equity",
            "debt_to_equity",
            "net_debt_to_ebit",
            "current_ratio",
            "fcf_yield",
            "earnings_yield",
            "ev_ebit",
            "ev_fcf",
            "buyback_yield",
            "share_dilution_pct",
            "source",
        }
