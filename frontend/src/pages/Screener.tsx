import React from 'react';
import { SlidersHorizontal, ArrowUpDown } from 'lucide-react';

export const Screener: React.FC = () => {
  const screenerResults = [
    { ticker: "AAPL", price: 172.50, fairValue: 195.00, upside: 13.0, quality: 85, valuation: 70, opportunity: 82.50 },
    { ticker: "MSFT", price: 395.20, fairValue: 420.00, upside: 6.2, quality: 90, valuation: 60, opportunity: 79.20 },
    { ticker: "GOOGL", price: 145.30, fairValue: 170.00, upside: 16.9, quality: 80, valuation: 80, opportunity: 80.00 },
    { ticker: "META", price: 490.50, fairValue: 510.00, upside: 3.9, quality: 88, valuation: 55, opportunity: 73.10 }
  ];

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">UNIVERSE SCREENER</h1>
          <span className="text-xs text-textSecondary font-medium">Filter quality stocks on sale</span>
        </div>
        <div className="flex items-center gap-3">
          <button className="bg-darkCard hover:bg-darkCardHover border border-[#1F2937] text-white font-semibold text-xs px-4 py-2 rounded-lg transition-all flex items-center gap-2">
            <SlidersHorizontal className="h-3.5 w-3.5" />
            Filters Panel
          </button>
        </div>
      </div>

      {/* Filter Presets Row */}
      <div className="grid grid-cols-5 gap-4 bg-darkCard border border-[#1F2937] p-4 rounded-lg">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min ROE</label>
          <select className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500">
            <option>&gt; 15%</option>
            <option>&gt; 10%</option>
            <option>&gt; 5%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min Revenue Growth</label>
          <select className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500">
            <option>&gt; 10%</option>
            <option>&gt; 5%</option>
            <option>&gt; 0%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Max Debt/Equity</label>
          <select className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500">
            <option>&lt; 100%</option>
            <option>&lt; 150%</option>
            <option>&lt; 200%</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Max PE Ratio</label>
          <select className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500">
            <option>&lt; 30</option>
            <option>&lt; 25</option>
            <option>&lt; 20</option>
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider">Min Margin of Safety</label>
          <select className="bg-darkBg border border-[#1F2937] text-white text-xs rounded p-1.5 w-full focus:outline-none focus:border-emerald-500">
            <option>&gt; 20%</option>
            <option>&gt; 10%</option>
            <option>&gt; 0%</option>
          </select>
        </div>
      </div>

      {/* Main Table Result */}
      <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                <th className="pb-3 flex items-center gap-1">Ticker <ArrowUpDown className="h-3 w-3" /></th>
                <th className="pb-3 text-right">Price</th>
                <th className="pb-3 text-right">Fair Value</th>
                <th className="pb-3 text-right">Upside %</th>
                <th className="pb-3 text-right">Quality Score</th>
                <th className="pb-3 text-right">Valuation Score</th>
                <th className="pb-3 text-right">Opp Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
              {screenerResults.map((stock) => (
                <tr key={stock.ticker} className="hover:bg-darkCardHover/40 transition-all cursor-pointer">
                  <td className="py-3.5 text-emerald-400 font-bold">{stock.ticker}</td>
                  <td className="py-3.5 text-right font-semibold text-white">${stock.price.toFixed(2)}</td>
                  <td className="py-3.5 text-right text-textSecondary">${stock.fairValue.toFixed(2)}</td>
                  <td className="py-3.5 text-right text-emerald-400">+{stock.upside.toFixed(1)}%</td>
                  <td className="py-3.5 text-right text-indigo-400">{stock.quality}</td>
                  <td className="py-3.5 text-right text-amber-400">{stock.valuation}</td>
                  <td className="py-3.5 text-right font-bold text-white">{stock.opportunity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

