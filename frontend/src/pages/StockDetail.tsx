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

  // Financials State
  const [financialsPeriod, setFinancialsPeriod] = useState<'annual' | 'quarterly'>('annual');
  const [financialsType, setFinancialsType] = useState<'income' | 'balance' | 'cash_flow'>('income');
  const [statements, setStatements] = useState<any>(null);
  const [statementsLoading, setStatementsLoading] = useState<boolean>(false);

  // Valuation State
  const [valuationData, setValuationData] = useState<any>(null);
  const [valuationLoading, setValuationLoading] = useState<boolean>(false);

  const ticker = selectedTicker || "AAPL";

  useEffect(() => {
    fetchStockDetails();
  }, [ticker]);

  useEffect(() => {
    if (activeTab === 'financials') {
      fetchFinancials();
    } else if (activeTab === 'valuation') {
      fetchValuation();
    }
  }, [ticker, activeTab, financialsPeriod]);

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

  const fetchFinancials = async () => {
    setStatementsLoading(true);
    try {
      const data = await api.getStatements(ticker, financialsPeriod);
      setStatements(data);
    } catch (err) {
      console.error("Failed to load financials statements:", err);
      setStatements(null);
    } finally {
      setStatementsLoading(false);
    }
  };

  const fetchValuation = async () => {
    setValuationLoading(true);
    try {
      const data = await api.getValuations(ticker);
      setValuationData(data);
    } catch (err) {
      console.error("Failed to load valuation snapshots:", err);
      setValuationData(null);
    } finally {
      setValuationLoading(false);
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
        if (activeTab === 'financials') fetchFinancials();
        if (activeTab === 'valuation') fetchValuation();
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

      {activeTab === 'financials' && (
        <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5 space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex gap-2 bg-[#111827] p-1 rounded-lg border border-[#1F2937]">
              {(['income', 'balance', 'cash_flow'] as const).map((type) => (
                <button
                  key={type}
                  onClick={() => setFinancialsType(type)}
                  className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${
                    financialsType === type
                      ? 'bg-emerald-500 text-white'
                      : 'text-textSecondary hover:text-white'
                  }`}
                >
                  {type === 'income' ? 'Income Statement' : type === 'balance' ? 'Balance Sheet' : 'Cash Flow'}
                </button>
              ))}
            </div>

            <div className="flex gap-2 bg-[#111827] p-1 rounded-lg border border-[#1F2937]">
              {(['annual', 'quarterly'] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setFinancialsPeriod(p)}
                  className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all capitalize ${
                    financialsPeriod === p
                      ? 'bg-emerald-500 text-white'
                      : 'text-textSecondary hover:text-white'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {statementsLoading ? (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary animate-pulse">Retrieving normalized statement data...</span>
            </div>
          ) : statements && statements.statements ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                    <th className="pb-3">Line Item (Normalized)</th>
                    {(() => {
                      const list = financialsType === 'income'
                        ? statements.statements.income_statements
                        : financialsType === 'balance'
                        ? statements.statements.balance_sheets
                        : statements.statements.cash_flow_statements;
                      return list?.map((stmt: any) => (
                        <th key={stmt.period_end_date} className="pb-3 text-right">
                          {new Date(stmt.period_end_date).toLocaleDateString(undefined, { year: 'numeric', month: 'short' })}
                        </th>
                      ));
                    })()}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1f2937]/50 text-xs font-medium text-white">
                  {(() => {
                    const list = financialsType === 'income'
                      ? statements.statements.income_statements
                      : financialsType === 'balance'
                      ? statements.statements.balance_sheets
                      : statements.statements.cash_flow_statements;

                    if (!list || list.length === 0) {
                      return (
                        <tr>
                          <td colSpan={5} className="py-6 text-center text-textSecondary">
                            No statement records available.
                          </td>
                        </tr>
                      );
                    }

                    // Extract available line items based on type
                    let items: { label: string; key: string; isBold?: boolean }[] = [];
                    if (financialsType === 'income') {
                      items = [
                        { label: "Total Revenue", key: "total_revenue", isBold: true },
                        { label: "Cost of Revenue", key: "cost_of_revenue" },
                        { label: "Gross Profit", key: "gross_profit", isBold: true },
                        { label: "Operating Expenses", key: "operating_expenses" },
                        { label: "Operating Income (EBIT)", key: "operating_income", isBold: true },
                        { label: "Interest Expense", key: "interest_expense" },
                        { label: "Income Before Tax", key: "income_before_tax" },
                        { label: "Net Income", key: "net_income", isBold: true },
                        { label: "EPS (Diluted)", key: "eps_diluted", isBold: true },
                      ];
                    } else if (financialsType === 'balance') {
                      items = [
                        { label: "Cash & Equivalents", key: "cash_and_equivalents" },
                        { label: "Total Current Assets", key: "total_current_assets", isBold: true },
                        { label: "Total Assets", key: "total_assets", isBold: true },
                        { label: "Short Term Debt", key: "short_term_debt" },
                        { label: "Long Term Debt", key: "long_term_debt" },
                        { label: "Total Current Liabilities", key: "total_current_liabilities", isBold: true },
                        { label: "Total Liabilities", key: "total_liabilities", isBold: true },
                        { label: "Total Equity", key: "total_equity", isBold: true },
                      ];
                    } else {
                      items = [
                        { label: "Net Income", key: "net_income" },
                        { label: "Depreciation & Amortization", key: "depreciation_and_amortization" },
                        { label: "Operating Cash Flow", key: "operating_cash_flow", isBold: true },
                        { label: "Capital Expenditure", key: "capital_expenditure" },
                        { label: "Free Cash Flow", key: "free_cash_flow", isBold: true },
                      ];
                    }

                    const formatNum = (val: any) => {
                      if (val === null || val === undefined) return "-";
                      if (Math.abs(val) > 1e9) return `${(val / 1e9).toFixed(2)}B`;
                      if (Math.abs(val) > 1e6) return `${(val / 1e6).toFixed(2)}M`;
                      return val.toLocaleString();
                    };

                    return items.map((item) => (
                      <tr key={item.key} className="hover:bg-darkCardHover/40 transition-all">
                        <td className={`py-3 ${item.isBold ? 'font-bold text-emerald-400' : 'text-textSecondary'}`}>
                          {item.label}
                        </td>
                        {list.map((stmt: any) => (
                          <td key={stmt.period_end_date} className={`py-3 text-right ${item.isBold ? 'font-bold text-white' : 'text-textSecondary'}`}>
                            {formatNum(stmt[item.key])}
                          </td>
                        ))}
                      </tr>
                    ));
                  })()}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary">No statement records available for this ticker.</span>
            </div>
          )}
        </div>
      )}

      {activeTab === 'valuation' && (
        <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5 space-y-6">
          <span className="text-xs font-bold text-textSecondary uppercase tracking-wider block">INTRINSIC VALUE MODEL COMPARISONS</span>

          {valuationLoading ? (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary animate-pulse">Running DCF and Owner Earnings models...</span>
            </div>
          ) : valuationData && valuationData.valuations ? (
            <div className="grid grid-cols-2 gap-6">
              {valuationData.valuations.map((val: any) => {
                const isPositive = val.margin_of_safety_pct > 0;
                return (
                  <div key={val.method} className="bg-darkBg border border-[#1f2937] p-5 rounded-lg space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-white uppercase tracking-wider">
                        {val.method === 'dcf' ? 'Discounted Cash Flow (DCF)' : "Owner Earnings Value"}
                      </span>
                      <Badge type={isPositive ? "success" : "danger"}>
                        {isPositive ? `+${val.margin_of_safety_pct.toFixed(1)}% MoS` : `${val.margin_of_safety_pct.toFixed(1)}% MoS`}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="bg-darkCard border border-[#1f2937]/50 p-2.5 rounded">
                        <span className="text-[10px] text-textSecondary font-bold block uppercase">Current Price</span>
                        <span className="text-lg font-extrabold text-white">${valuationData.current_price.toFixed(2)}</span>
                      </div>
                      <div className="bg-darkCard border border-[#1f2937]/50 p-2.5 rounded">
                        <span className="text-[10px] text-textSecondary font-bold block uppercase">Intrinsic Value (Base)</span>
                        <span className="text-lg font-extrabold text-emerald-400">${val.base_case_value.toFixed(2)}</span>
                      </div>
                    </div>

                    {/* Gauge style bar */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-[10px] text-textSecondary font-bold uppercase">
                        <span>Bear Case: ${val.bear_case_value.toFixed(1)}</span>
                        <span>Bull Case: ${val.bull_case_value.toFixed(1)}</span>
                      </div>
                      <div className="w-full bg-[#111827] h-2 rounded-full overflow-hidden border border-[#1f2937]">
                        <div
                          className="bg-emerald-500 h-full rounded-full"
                          style={{
                            width: `${Math.min(100, Math.max(0, ((valuationData.current_price - val.bear_case_value) / (val.bull_case_value - val.bear_case_value)) * 100))}%`
                          }}
                        />
                      </div>
                    </div>

                    {/* Assumptions list */}
                    <div className="bg-darkCard border border-[#1f2937]/50 p-3 rounded-lg text-xs space-y-1.5">
                      <span className="text-[10px] text-textSecondary font-bold block uppercase mb-1">Model Assumptions</span>
                      {Object.entries(val.assumptions || {}).map(([k, v]: [string, any]) => (
                        <div key={k} className="flex justify-between">
                          <span className="text-textSecondary capitalize">{k.replace(/_/g, ' ')}</span>
                          <span className="text-white font-semibold">
                            {typeof v === 'number' && v < 1 ? `${(v * 100).toFixed(1)}%` : typeof v === 'number' ? v.toLocaleString() : String(v)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary">No valuation metrics calculated yet.</span>
            </div>
          )}
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

