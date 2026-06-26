import React, { useState, useEffect } from 'react';
import { Badge } from '../components/Badge';
import { 
  TrendingUp, 
  ShieldAlert, 
  BookmarkCheck,
  Layers,
  RefreshCw
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar 
} from 'recharts';
import { api } from '../lib/api';

interface StockDetailProps {
  selectedTicker: string;
}

export const StockDetail: React.FC<StockDetailProps> = ({ selectedTicker }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'financials' | 'valuation' | 'chart'>('overview');
  const [scoreHistory, setScoreHistory] = useState<any[]>([]);
  const [latestScore, setLatestScore] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const ticker = selectedTicker || "AAPL";

  useEffect(() => {
    fetchStockDetails();
  }, [ticker]);

  const fetchStockDetails = async () => {
    setLoading(true);
    try {
      // 1. Pull historical score snapshots (time-series)
      const history = await api.getScoreHistory(ticker);
      setScoreHistory(history);

      if (history.length > 0) {
        // Sort history by date desc to find the newest score
        const sorted = [...history].sort((a: any, b: any) => new Date(b.snapshot_date).getTime() - new Date(a.snapshot_date).getTime());
        setLatestScore(sorted[0]);
      } else {
        setLatestScore(null);
      }
    } catch (err) {
      console.error("Failed to load stock detail history:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleManualTrigger = async () => {
    setLoading(true);
    try {
      // Force trigger ingestion & recalculation in background task
      await api.triggerRefresh(ticker);
      alert(`Recalculation started for ${ticker}. Give it a few seconds to update, then click refresh!`);
      setTimeout(() => {
        fetchStockDetails();
      }, 5000); // Wait 5 seconds before checking
    } catch (err) {
      console.error("Trigger failed:", err);
    }
  };

  // Safe mapping of the latest score components to the Radar data
  const radarData = latestScore ? [
    { subject: 'Quality', value: parseFloat(latestScore.quality_score), fullMark: 100 },
    { subject: 'Valuation', value: parseFloat(latestScore.valuation_score), fullMark: 100 },
    { subject: 'Discount', value: parseFloat(latestScore.discount_score), fullMark: 100 },
    { subject: 'Analyst', value: parseFloat(latestScore.analyst_score), fullMark: 100 }
  ] : [
    { subject: 'Quality', value: 0, fullMark: 100 },
    { subject: 'Valuation', value: 0, fullMark: 100 },
    { subject: 'Discount', value: 0, fullMark: 100 },
    { subject: 'Analyst', value: 0, fullMark: 100 }
  ];

  return (
    <div className="space-y-6">
      {/* Header Profile Section */}
      <div className="bg-[#111827] border border-[#1F2937] p-6 rounded-lg flex justify-between items-center">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-3xl font-black tracking-tight text-white">{ticker}</span>
            {latestScore && (
              <Badge type={parseFloat(latestScore.opportunity_score) >= 70 ? "success" : "info"}>
                OPPORTUNITY SCORE: {parseFloat(latestScore.opportunity_score).toFixed(1)}
              </Badge>
            )}
          </div>
          <span className="text-sm font-semibold text-textSecondary">NASDAQ • SEC Snapshot System</span>
        </div>
        <div>
          <button 
            onClick={handleManualTrigger}
            disabled={loading}
            className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white font-semibold text-xs px-4 py-2.5 rounded-lg transition-all flex items-center gap-2"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Ingesting...' : 'Force Raw Recompute'}
          </button>
        </div>
      </div>

      {/* Tabs navigation */}
      <div className="flex border-b border-[#1F2937] gap-6">
        {(['overview', 'financials', 'valuation', 'chart'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-bold capitalize transition-all focus:outline-none border-b-2 px-1 ${
              activeTab === tab 
                ? 'border-emerald-500 text-emerald-400' 
                : 'border-transparent text-textSecondary hover:text-white'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-3 gap-6">
          {/* Quality Radar Chart */}
          <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5 flex flex-col items-center justify-center min-h-[300px]">
            <span className="text-xs font-bold text-textSecondary uppercase tracking-wider self-start mb-4">SCORE RATIO ANALYSIS</span>
            {latestScore ? (
              <ResponsiveContainer width="100%" height={220}>
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                  <PolarGrid stroke="#1F2937" />
                  <PolarAngleAxis dataKey="subject" stroke="#9CA3AF" fontSize={11} fontWeight="bold" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#1F2937" />
                  <Radar name={ticker} dataKey="value" stroke="#10B981" fill="#10B981" fillOpacity={0.4} />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <span className="text-xs text-textSecondary text-center">No calculated score found for this ticker yet. Click "Force Raw Recompute" at the top right to calculate now!</span>
            )}
          </div>

          {/* Core Metrics Grid */}
          <div className="col-span-2 bg-darkCard border border-[#1F2937] rounded-lg p-5 space-y-4">
            <span className="text-xs font-bold text-textSecondary uppercase tracking-wider block">SCORE COMPONENT BREAKDOWN</span>
            
            {latestScore ? (
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-darkBg border border-[#1f2937] p-4 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Business Quality Score</span>
                    <span className="text-lg font-bold text-white">{parseFloat(latestScore.quality_score).toFixed(0)} / 100</span>
                  </div>
                  <BookmarkCheck className="h-5 w-5 text-emerald-400" />
                </div>

                <div className="bg-darkBg border border-[#1f2937] p-4 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Valuation Score</span>
                    <span className="text-lg font-bold text-white">{parseFloat(latestScore.valuation_score).toFixed(0)} / 100</span>
                  </div>
                  <Layers className="h-5 w-5 text-indigo-400" />
                </div>

                <div className="bg-darkBg border border-[#1f2937] p-4 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Discount Drawdown Score</span>
                    <span className="text-lg font-bold text-white">{parseFloat(latestScore.discount_score).toFixed(0)} / 100</span>
                  </div>
                  <TrendingUp className="h-5 w-5 text-teal-400" />
                </div>

                <div className="bg-darkBg border border-[#1f2937] p-4 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Analyst Rating Score</span>
                    <span className="text-lg font-bold text-white">{parseFloat(latestScore.analyst_score).toFixed(0)} / 100</span>
                  </div>
                  <ShieldAlert className="h-5 w-5 text-amber-400" />
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center py-10">
                <span className="text-xs text-textSecondary">Calculated score breakdown will sit here after ingestion occurs.</span>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'chart' && (
        <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5 min-h-[350px]">
          <span className="text-xs font-bold text-textSecondary uppercase tracking-wider block mb-6">OPPORTUNITY SCORE TIME-SERIES HISTORY</span>
          {scoreHistory.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={scoreHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
                <XAxis dataKey="snapshot_date" stroke="#9CA3AF" fontSize={11} fontWeight="bold" />
                <YAxis domain={[0, 100]} stroke="#9CA3AF" fontSize={11} fontWeight="bold" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#161E2E', border: '1px solid #1F2937', borderRadius: '8px' }}
                  labelStyle={{ fontWeight: 'bold', color: '#fff' }}
                />
                <Line type="monotone" dataKey="opportunity_score" stroke="#10B981" strokeWidth={3} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary">Time-series trend lines will display as you build up database snapshots over time.</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
