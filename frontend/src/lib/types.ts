export interface Stock {
  ticker: string;
  company_name: string;
  sector: string | null;
  industry: string | null;
  exchange: string | null;
  country: string | null;
  market_cap: number | null;
  is_active: boolean;
}

export interface StockPrice {
  ticker: string;
  price_date: string;
  close_price: number;
  below_52w_high_pct: number;
}

export interface FinancialMetric {
    ticker: string;
    snapshot_date: string;
    forward_pe: number;
    pe_ratio: number;
    ps_ratio: number;
    peg_ratio: number;
    revenue_growth: number;
    eps_growth: number;
    ebit_growth: number;
    roe: number;
    roic: number;
    ebit_margin: number;
    gross_margin: number;
    net_margin: number;
    debt_equity: number;
    current_ratio: number;
}

export interface AnalystData {
    ticker: string;
    snapshot_date: string;
    target_price_avg: number;
    target_price_high: number;
    target_price_low: number;
    target_upside_pct: number;
    strong_buy: number;
    buy: number;
    hold: number;
    sell: number;
    strong_sell: number;
    consensus_rating: string;
}

export interface StockScore {
  ticker: string;
  snapshot_date: string;
  quality_score: number;
  valuation_score: number;
  discount_score: number;
  analyst_score: number;
  opportunity_score: number;
  score_version: string;
}

export interface WatchlistItem {
  id: number;
  ticker: string;
  note: string | null;
  created_at: string;
  company_name: string | null;
}
