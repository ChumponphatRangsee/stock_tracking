import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Search, 
  RefreshCw, 
  AlertTriangle,
  Play
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { api } from '../lib/api';

interface DashboardProps {
  onNavigateToStock: (ticker: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigateToStock }) => {
  const [topOpportunities, setTopOpportunities] = useState<any[]>([]);
  const [watchlistCount, setWatchlistCount] = useState<number>(0);
  const [matchingCount, setMatchingCount] = useState<number>(0);
  const [nearBuyCount, setNearBuyCount] = useState<number>(0);
  const [recentPipelineLogs, setRecentPipelineLogs] = useState<any[]>([]);
  const [searchTicker, setSearchTicker] = useState<string>("");

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // 1. Fetch top opportunities (ranked by opportunity_score desc)
      const scores = await api.getTopOpportunities(10);
      setTopOpportunities(scores);

      // 2. Fetch watchlist items count
      const watchlist = await api.getWatchlist();
      setWatchlistCount(watchlist.length);

      // 3. Count matching quality stocks (Quality Score > 65)
      const matching = scores.filter((item: any) => parseFloat(item.quality_score) > 65);
      setMatchingCount(matching.length);

      // 4. Calculate stocks "Near Buy Zone" (arbitrary: margin_of_safety_pct is positive but within 15% or high scores)
      // Since we don't have valuation list here directly, let's count stocks where margin_of_safety_score is strong (> 50)
      const nearBuy = scores.filter((item: any) => parseFloat(item.margin_of_safety_score || 0) > 50);
      setNearBuyCount(nearBuy.length);

      // 5. Build dynamic logs from recently fetched stocks
      const fakeLogs = scores.slice(0, 3).map((item: any) => ({
        ticker: item.ticker,
        title: `${item.ticker} Pipeline Complete`,
        desc: `Score evaluated: ${parseFloat(item.opportunity_score).toFixed(1)}`,
        time: "Just now"
      }));
      setRecentPipelineLogs(fakeLogs);

    } catch (err) {
      console.error("Failed to pull dashboard analytics:", err);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTicker.trim()) {
      onNavigateToStock(searchTicker.trim().toUpperCase());
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">COCKPIT OVERVIEW</h1>
          <span className="text-xs text-textSecondary font-medium">Real-time market analytics summary</span>
        </div>
        <div className="flex items-center gap-3">
          <form onSubmit={handleSearchSubmit} className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-textSecondary" />
            <input
              type="text"
              placeholder="Query ticker..."
              value={searchTicker}
              onChange={(e) => setSearchTicker(e.target.value)}
              className="bg-[#111827] border border-[#1F2937] text-sm text-white rounded-lg pl-9 pr-4 py-2 w-64 focus:outline-none focus:border-emerald-500 transition-all"
            />
          </form>
          <button 
            onClick={fetchDashboardData}
            className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold text-xs px-4 py-2 rounded-lg transition-all flex items-center gap-2"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh Overview
          </button>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-4 gap-4">
        <MetricCard title="Total Watchlist" value={watchlistCount} subValue="Tracked assets" icon={TrendingUp} />
        <MetricCard title="Matching Stocks" value={matchingCount} subValue="Quality score > 65" icon={TrendingUp} />
        <MetricCard title="Near Buy Zone" value={nearBuyCount} subValue="Strong Margin of Safety" icon={TrendingUp} />
        <MetricCard title="Triggered Alerts" value="Live Monitoring" subValue="Cockpit Active" icon={AlertTriangle} />
      </div>

      {/* Main split grid */}
      <div className="grid grid-cols-3 gap-6">
        {/* Left 2 columns: Top Opportunities */}
        <div className="col-span-2 bg-darkCard border border-[#1F2937] rounded-lg p-5 space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold tracking-tight text-white">TOP MATCHING OPPORTUNITIES</span>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                  <th className="pb-3">Ticker</th>
                  <th className="pb-3 text-right">Quality</th>
                  <th className="pb-3 text-right">Valuation</th>
                  <th className="pb-3 text-right">MoS Score</th>
                  <th className="pb-3 text-right">Risk Score</th>
                  <th className="pb-3 text-right">Opportunity Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
                {topOpportunities.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-textSecondary text-xs">
                      No data ingested yet. Query a ticker in the search bar above to trigger your first run!
                    </td>
                  </tr>
                ) : (
                  topOpportunities.map((stock) => (
                    <tr 
                      key={stock.ticker}
                      onClick={() => onNavigateToStock(stock.ticker)}
                      className="hover:bg-darkCardHover/40 cursor-pointer transition-all"
                    >
                      <td className="py-3 text-emerald-400 font-bold">{stock.ticker}</td>
                      <td className="py-3 text-right text-indigo-400">{parseFloat(stock.quality_score).toFixed(0)}</td>
                      <td className="py-3 text-right text-amber-400">{parseFloat(stock.valuation_score).toFixed(0)}</td>
                      <td className="py-3 text-right text-teal-400">{parseFloat(stock.margin_of_safety_score || 0).toFixed(0)}</td>
                      <td className="py-3 text-right text-rose-400">{parseFloat(stock.risk_score || 0).toFixed(0)}</td>
                      <td className="py-3 text-right font-bold text-white text-base">{parseFloat(stock.opportunity_score).toFixed(2)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right 1 column: Recent Alerts list */}
        <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5 space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold tracking-tight text-white">RECENT SYSTEM LOGS</span>
          </div>

          <div className="space-y-3">
            {recentPipelineLogs.length === 0 ? (
            <div className="bg-[#111827] border border-[#1F2937] p-3 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">System Status</span>
                <span className="text-sm font-semibold text-white">Cockpit Active</span>
                  <span className="text-xs text-textSecondary block mt-0.5">Ready for ingestion</span>
              </div>
              <Play className="h-4 w-4 text-emerald-400 animate-pulse" />
            </div>
            ) : (
              recentPipelineLogs.map((log, index) => (
                <div key={index} className="bg-[#111827] border border-[#1F2937] p-3 rounded-lg flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">{log.time}</span>
                    <span className="text-sm font-semibold text-white">{log.title}</span>
                    <span className="text-xs text-textSecondary block mt-0.5">{log.desc}</span>
            </div>
                  <Play className="h-4 w-4 text-emerald-400" />
          </div>
              ))
            )}
      </div>
    </div>
      </div>
    </div>
  );
};

