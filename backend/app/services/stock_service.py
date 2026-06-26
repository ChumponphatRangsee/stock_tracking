from datetime import date
from sqlalchemy.orm import Session
from app.models.stock_price import StockPrice
from app.models.financial_metric import FinancialMetric
from app.models.analyst_data import AnalystData
from app.models.stock_score import StockScore

# Import our modular scoring calculators
from app.scoring.quality_score import calculate_quality_score
from app.scoring.valuation_score import calculate_valuation_score
from app.scoring.discount_score import calculate_discount_score
from app.scoring.analyst_score import calculate_analyst_score
from app.scoring.opportunity_score import calculate_opportunity_score

from sqlalchemy.dialects.postgresql import insert

class StockService:
    """
    Business Logic Layer for managing stocks.
    Specifically reads raw snapshots and computes the modular opportunity scores.
    """
    def __init__(self, db: Session):
        self.db = db

    def calculate_and_save_scores(self, ticker: str) -> StockScore:
        """
        Pulls the latest snapshot metrics for a ticker,
        calculates the 5 scores, and saves them to the stock_scores table.
        """
        print(f"Calculating opportunity score for {ticker}...")
        today = date.today()

        # 1. Fetch latest metric snapshot
        metric = self.db.query(FinancialMetric).filter(
            FinancialMetric.ticker == ticker
        ).order_by(FinancialMetric.snapshot_date.desc()).first()

        # 2. Fetch latest price snapshot
        price = self.db.query(StockPrice).filter(
            StockPrice.ticker == ticker
        ).order_by(StockPrice.price_date.desc()).first()

        # 3. Fetch latest analyst snapshot
        analyst = self.db.query(AnalystData).filter(
            AnalystData.ticker == ticker
        ).order_by(AnalystData.snapshot_date.desc()).first()

        # --- Calculations ---
        
        # A. Quality Score
        q_score = 0.0
        if metric:
            q_score = calculate_quality_score(
                roe=float(metric.roe) if metric.roe is not None else None,
                roic=float(metric.roic) if metric.roic is not None else None,
                ebit_margin=float(metric.ebit_margin) if metric.ebit_margin is not None else None,
                debt_equity=float(metric.debt_equity) if metric.debt_equity is not None else None,
                rev_growth=float(metric.revenue_growth) if metric.revenue_growth is not None else None,
                ebit_growth=float(metric.ebit_growth) if metric.ebit_growth is not None else None
            )

        # B. Valuation Score
        v_score = 0.0
        if metric:
            v_score = calculate_valuation_score(
                forward_pe=float(metric.forward_pe) if metric.forward_pe is not None else None,
                pe_ratio=float(metric.pe_ratio) if metric.pe_ratio is not None else None,
                ps_ratio=float(metric.ps_ratio) if metric.ps_ratio is not None else None,
                peg_ratio=float(metric.peg_ratio) if metric.peg_ratio is not None else None
            )

        # C. Discount Score
        d_score = 0.0
        if price:
            d_score = calculate_discount_score(
                below_52w_high_pct=float(price.below_52w_high_pct) if price.below_52w_high_pct is not None else None
            )

        # D. Analyst Score
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

        # E. Final Opportunity Score
        opp_score = calculate_opportunity_score(
            quality_score=q_score,
            valuation_score=v_score,
            discount_score=d_score,
            analyst_score=a_score
        )

        # 4. Upsert/Insert Score Snapshot
        score_data = {
            "quality_score": round(q_score, 2),
            "valuation_score": round(v_score, 2),
            "discount_score": round(d_score, 2),
            "analyst_score": round(a_score, 2),
            "opportunity_score": round(opp_score, 2),
            "score_version": "v1"
        }

        stmt = insert(StockScore).values(
            ticker=ticker,
            snapshot_date=today,
            **score_data
        ).on_conflict_do_update(
            index_elements=['ticker', 'snapshot_date', 'score_version'],
            set_=score_data
        )
        
        self.db.execute(stmt)
        self.db.commit()
        
        print(f"Calculations complete for {ticker}. Opp Score: {round(opp_score, 2)}")
        
        # Return the active score object
        return self.db.query(StockScore).filter(
            StockScore.ticker == ticker,
            StockScore.snapshot_date == today,
            StockScore.score_version == "v1"
        ).first()
