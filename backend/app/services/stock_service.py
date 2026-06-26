from datetime import date
from sqlalchemy.orm import Session
from app.models.stock_price import StockPrice
from app.models.analyst_data import AnalystData
from app.models.stock_score import StockScore
from app.repositories.metric_repository import MetricRepository
from app.repositories.score_repository import ScoreRepository
from app.repositories.valuation_repository import ValuationRepository
from app.scoring.quality_score import calculate_quality_score
from app.scoring.valuation_score import calculate_valuation_score
from app.scoring.discount_score import calculate_discount_score
from app.scoring.analyst_score import calculate_analyst_score
from app.scoring.margin_of_safety_score import calculate_margin_of_safety_score
from app.scoring.trend_score import calculate_trend_score
from app.scoring.risk_score import calculate_risk_score
from app.scoring.opportunity_score import calculate_opportunity_score

class StockService:
    """
    Reads the latest metric, price, analyst, and valuation snapshots to produce scores.
    """
    def __init__(self, db: Session):
        self.db = db
        self.metric_repository = MetricRepository(db)
        self.valuation_repository = ValuationRepository(db)
        self.score_repository = ScoreRepository(db)

    def calculate_and_save_scores(self, ticker: str) -> StockScore:
        print(f"Calculating opportunity score for {ticker}...")
        today = date.today()

        metric = self.metric_repository.latest(ticker)

        price = self.db.query(StockPrice).filter(
            StockPrice.ticker == ticker
        ).order_by(StockPrice.price_date.desc()).first()

        analyst = self.db.query(AnalystData).filter(
            AnalystData.ticker == ticker
        ).order_by(AnalystData.snapshot_date.desc()).first()
        valuation = self.valuation_repository.latest_preferred(ticker)

        q_score = 0.0
        if metric:
            q_score = calculate_quality_score(
                roe=float(metric.roe) if metric.roe is not None else None,
                roic=float(metric.roic) if metric.roic is not None else None,
                ebit_margin=float(metric.operating_margin or metric.ebit_margin) if (metric.operating_margin is not None or metric.ebit_margin is not None) else None,
                debt_equity=float(metric.debt_to_equity or metric.debt_equity) if (metric.debt_to_equity is not None or metric.debt_equity is not None) else None,
                rev_growth=float(metric.revenue_growth_3y_cagr or metric.revenue_growth or 0.0),
                ebit_growth=float(metric.ebit_growth_3y_cagr or metric.ebit_growth or 0.0),
            )

        v_score = 0.0
        if metric:
            v_score = calculate_valuation_score(
                fcf_yield=float(metric.fcf_yield) if metric.fcf_yield is not None else None,
                earnings_yield=float(metric.earnings_yield) if metric.earnings_yield is not None else None,
                ev_ebit=float(metric.ev_ebit) if metric.ev_ebit is not None else None,
                ev_fcf=float(metric.ev_fcf) if metric.ev_fcf is not None else None,
            )

        d_score = 0.0
        if price:
            d_score = calculate_discount_score(
                below_52w_high_pct=float(price.below_52w_high_pct) if price.below_52w_high_pct is not None else None
            )

        a_score = 0.0
        if analyst:
            a_score = calculate_analyst_score(
                target_upside_pct=float(analyst.target_upside_pct) if analyst.target_upside_pct is not None else None,
                strong_buy=analyst.strong_buy or 0,
                buy=analyst.buy or 0,
                hold=analyst.hold or 0,
                sell=analyst.sell or 0,
                strong_sell=analyst.strong_sell or 0
            )

        t_score = 0.0
        r_score = 100.0
        mos_score = 0.0
        if metric:
            t_score = calculate_trend_score(
                revenue_growth_3y_cagr=float(metric.revenue_growth_3y_cagr) if metric.revenue_growth_3y_cagr is not None else None,
                ebit_growth_3y_cagr=float(metric.ebit_growth_3y_cagr) if metric.ebit_growth_3y_cagr is not None else None,
                fcf_growth_3y_cagr=float(metric.fcf_growth_3y_cagr) if metric.fcf_growth_3y_cagr is not None else None,
                operating_margin=float(metric.operating_margin or metric.ebit_margin) if (metric.operating_margin is not None or metric.ebit_margin is not None) else None,
                fcf_margin=float(metric.fcf_margin) if metric.fcf_margin is not None else None,
            )
            r_score = calculate_risk_score(
                debt_to_equity=float(metric.debt_to_equity or metric.debt_equity) if (metric.debt_to_equity is not None or metric.debt_equity is not None) else None,
                revenue_growth_1y=float(metric.revenue_growth_1y or metric.revenue_growth or 0.0),
                ebit_growth_3y_cagr=float(metric.ebit_growth_3y_cagr or metric.ebit_growth or 0.0),
                fcf_growth_3y_cagr=float(metric.fcf_growth_3y_cagr or 0.0),
                fcf_margin=float(metric.fcf_margin or 0.0),
                share_dilution_pct=float(metric.share_dilution_pct or 0.0),
            )

        if valuation and valuation.margin_of_safety_pct is not None:
            mos_score = calculate_margin_of_safety_score(float(valuation.margin_of_safety_pct))

        opp_score = calculate_opportunity_score(
            quality_score=q_score,
            valuation_score=v_score,
            margin_of_safety_score=mos_score,
            trend_score=t_score,
            risk_score=r_score,
            analyst_score=a_score,
        )

        score_data = {
            "ticker": ticker,
            "snapshot_date": today,
            "quality_score": round(q_score, 2),
            "valuation_score": round(v_score, 2),
            "discount_score": round(d_score, 2),
            "analyst_score": round(a_score, 2),
            "trend_score": round(t_score, 2),
            "risk_score": round(r_score, 2),
            "margin_of_safety_score": round(mos_score, 2),
            "opportunity_score": round(opp_score, 2),
            "score_version": "v2_vi",
        }
        self.score_repository.save_snapshot(score_data)
        self.db.commit()
        
        print(f"Calculations complete for {ticker}. Opp Score: {round(opp_score, 2)}")
        
        return self.db.query(StockScore).filter(
            StockScore.ticker == ticker,
            StockScore.snapshot_date == today,
            StockScore.score_version == "v2_vi"
        ).first()
