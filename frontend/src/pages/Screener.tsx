import React from 'react';
import { SlidersHorizontal, ArrowUpDown } from 'lucide-react';
import { api } from '../lib/api';

interface ScreenerProps {
  onNavigateToStock: (ticker: string) => void;
}
export const Screener: React.FC<ScreenerProps> = ({ onNavigateToStock }) => {
  const [stocksList, setStocksList] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState<boolean>(false);

  // Filter States
  const [minRoe, setMinRoe] = React.useState<number>(0);
  const [minRevGrowth, setMinRevGrowth] = React.useState<number>(0);
  const [maxDebtEquity, setMaxDebtEquity] = React.useState<number>(9999);
  const [maxPe, setMaxPe] = React.useState<number>(9999);
  const [minMos, setMinMos] = React.useState<number>(-999);

  React.useEffect(() => {
    fetchScreenerData();
  }, []);

  const fetchScreenerData = async () => {
    setLoading(true);
    try {
      // 1. Fetch latest evaluated opportunity scores
      const latestScores = await api.getLatestScores();

      // 2. To get current PE, ROE, margins, etc. we would ideally join details,
      // but to preserve performance we can query individual metrics/valuations for each stock.
      // Since it's a small watchlist stock monitor system (Quota defense), we can fetch the metric snapshots in parallel.
      const enriched = await Promise.all(
        latestScores.map(async (score: any) => {
          try {
            // Fetch metric and valuation
            const metric = await api.getStocks().then(res => res.find((s: any) => s.ticker === score.ticker));
            const vals = await api.getValuations(score.ticker).catch(() => null);
            const dcfVal = vals?.valuations?.find((v: any) => v.method === 'dcf');

            // Fetch individual metrics to do filters
            const metDetail = await clientGetMetrics(score.ticker).catch(() => null);

            return {
              ticker: score.ticker,
              price: vals?.current_price || 0.0,
              fairValue: dcfVal?.base_case_value || 0.0,
              upside: dcfVal?.margin_of_safety_pct || 0.0,
              quality: parseFloat(score.quality_score),
              valuation: parseFloat(score.valuation_score),
              opportunity: parseFloat(score.opportunity_score),
              roe: metDetail?.roe || 0.0,
              revGrowth: metDetail?.revenue_growth_3y_cagr || metDetail?.revenue_growth || 0.0,
              debtEquity: metDetail?.debt_to_equity || metDetail?.debt_equity || 0.0,
              pe: metDetail?.pe_ratio || metDetail?.forward_pe || 999
            };
          } catch {
            return {
              ticker: score.ticker,
              price: 0,
              fairValue: 0,
              upside: 0,
              quality: parseFloat(score.quality_score),
              valuation: parseFloat(score.valuation_score),
              opportunity: parseFloat(score.opportunity_score),
              roe: 0,
              revGrowth: 0,
              debtEquity: 0,
              pe: 999
            };
          }
        })
      );
      setStocksList(enriched);
    } catch (err) {
      console.error("Failed to fetch screener data:", err);
    } finally {
      setLoading(false);
    }
  };

  // Quick custom helper to get metrics
  const clientGetMetrics = async (ticker: string) => {
    const res = await api.getStock(ticker); // In api.ts, this hits /stocks/{ticker}
    // Let's directly query /metrics/{ticker}
    const rawRes = await fetch(`http://localhost:8000/api/metrics/${ticker}`);
    if (rawRes.ok) return await rawRes.json();
    return null;
  };

  // Reactive Client-Side Filtering
  const filteredStocks = stocksList.filter((stock) => {
    const passRoe = (stock.roe * 100) >= minRoe;
    const passRev = (stock.revGrowth * 100) >= minRevGrowth;
    const passDebt = (stock.debtEquity * 100) <= maxDebtEquity;
    const passPe = stock.pe <= maxPe;
    const passMos = stock.upside >= minMos;

    return passRoe && passRev && passDebt && passPe && passMos;
  });

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">UNIVERSE SCREENER</h1>
          <span className="text-xs text-textSecondary font-medium">Filter quality stocks on sale</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchScreenerData}
            className="bg-darkCard hover:bg-darkCardHover border border-[#1F2937] text-white font-semibold text-xs px-4 py-2 rounded-lg transition-all flex items-center gap-2"
          >
            <SlidersHorizontal className="h-3.5 w-3.5" />
            Refresh Screener
          </button>
        </div>
      </div>

      {/* Filter Presets Row */}
      <div className="grid grid-cols-5 gap-4 bg-darkCard border border-[#1F2937] p-4 rounded-lg">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min ROE</label>
          <select
            onChange={(e) => setMinRoe(parseFloat(e.target.value))}
            className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500"
          >
            <option value="0">Any ROE</option>
            <option value="15">&gt; 15%</option>
            <option value="10">&gt; 10%</option>
            <option value="5">&gt; 5%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min Revenue Growth</label>
          <select
            onChange={(e) => setMinRevGrowth(parseFloat(e.target.value))}
            className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500"
          >
            <option value="0">Any Growth</option>
            <option value="10">&gt; 10%</option>
            <option value="5">&gt; 5%</option>
            <option value="0">&gt; 0%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Max Debt/Equity</label>
          <select
            onChange={(e) => setMaxDebtEquity(parseFloat(e.target.value))}
            className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500"
          >
            <option value="9999">Any Debt</option>
            <option value="100">&lt; 100%</option>
            <option value="150">&lt; 150%</option>
            <option value="200">&lt; 200%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Max PE Ratio</label>
          <select
            onChange={(e) => setMaxPe(parseFloat(e.target.value))}
            className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500"
          >
            <option value="9999">Any PE</option>
            <option value="30">&lt; 30</option>
            <option value="25">&lt; 25</option>
            <option value="20">&lt; 20</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min Margin of Safety</label>
          <select
            onChange={(e) => setMinMos(parseFloat(e.target.value))}
            className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500"
          >
            <option value="-999">Any MoS</option>
            <option value="20">&gt; 20%</option>
            <option value="10">&gt; 10%</option>
            <option value="0">&gt; 0%</option>
          </select>
        </div>
      </div>

      {/* Main Table Result */}
      <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5">
        <div className="overflow-x-auto">
          {loading ? (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary animate-pulse">Running screening criteria on active stocks...</span>
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                  <th className="pb-3 flex items-center gap-1">Ticker <ArrowUpDown className="h-3 w-3" /></th>
                  <th className="pb-3 text-right">Price</th>
                  <th className="pb-3 text-right">Fair Value (DCF)</th>
                  <th className="pb-3 text-right">Margin of Safety</th>
                  <th className="pb-3 text-right">Quality Score</th>
                  <th className="pb-3 text-right">Valuation Score</th>
                  <th className="pb-3 text-right">Opp Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
                {filteredStocks.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-6 text-center text-textSecondary text-xs">
                      No stocks in monitored universe match the selected screening criteria.
                    </td>
                  </tr>
                ) : (
                  filteredStocks.map((stock) => (
                    <tr
                      key={stock.ticker}
                      onClick={() => onNavigateToStock(stock.ticker)}
                      className="hover:bg-darkCardHover/40 transition-all cursor-pointer"
                    >
                      <td className="py-3.5 text-emerald-400 font-bold">{stock.ticker}</td>
                      <td className="py-3.5 text-right font-semibold text-white">
                        {stock.price > 0 ? `$${stock.price.toFixed(2)}` : 'N/A'}
                      </td>
                      <td className="py-3.5 text-right text-textSecondary">
                        {stock.fairValue > 0 ? `$${stock.fairValue.toFixed(2)}` : 'N/A'}
                      </td>
                      <td className={`py-3.5 text-right font-bold ${stock.upside > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {stock.upside > -99 ? `${stock.upside.toFixed(1)}%` : 'N/A'}
                      </td>
                      <td className="py-3.5 text-right text-indigo-400">{stock.quality.toFixed(0)}</td>
                      <td className="py-3.5 text-right text-amber-400">{stock.valuation.toFixed(0)}</td>
                      <td className="py-3.5 text-right font-bold text-white text-base">{stock.opportunity.toFixed(1)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

