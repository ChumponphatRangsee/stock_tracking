import React from 'react';
import { Badge } from '../components/Badge';
import { PlusCircle, ToggleLeft } from 'lucide-react';

export const Alerts: React.FC = () => {
  const alertRules = [
    { ticker: "AAPL", type: "Price drops below fair value", target: 195.00, current: 172.50, status: "Triggered", date: "06-25 16:32" },
    { ticker: "MSFT", type: "PE drops below target", target: 30.0, current: 35.10, status: "Active", date: "-" },
    { ticker: "GOOGL", type: "Margin of safety > 20%", target: 20.0, current: 14.50, status: "Active", date: "-" }
  ];

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">ALERTS MANAGER</h1>
          <span className="text-xs text-textSecondary font-medium">Configure cockpit triggers</span>
        </div>
        <div className="flex items-center gap-3">
          <button className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold text-xs px-4 py-2 rounded-lg transition-all flex items-center gap-2">
            <PlusCircle className="h-3.5 w-3.5" />
            Create Alert
          </button>
        </div>
      </div>

      {/* Main Alerts Table */}
      <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                <th className="pb-3">Ticker</th>
                <th className="pb-3">Alert Condition</th>
                <th className="pb-3 text-right">Target Level</th>
                <th className="pb-3 text-right">Current Price</th>
                <th className="pb-3 text-center">Status</th>
                <th className="pb-3 text-center">Last Triggered</th>
                <th className="pb-3 text-center">Toggle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
              {alertRules.map((alert) => (
                <tr key={alert.ticker} className="hover:bg-darkCardHover/40 transition-all">
                  <td className="py-3.5 text-emerald-400 font-bold">{alert.ticker}</td>
                  <td className="py-3.5 text-white">{alert.type}</td>
                  <td className="py-3.5 text-right text-white font-bold">{alert.target.toFixed(2)}</td>
                  <td className="py-3.5 text-right text-textSecondary">${alert.current.toFixed(2)}</td>
                  <td className="py-3.5 text-center">
                    <Badge type={alert.status === "Triggered" ? "danger" : "info"}>
                      {alert.status}
                    </Badge>
                  </td>
                  <td className="py-3.5 text-center text-textSecondary">{alert.date}</td>
                  <td className="py-3.5 text-center">
                    <button className="text-emerald-400 hover:text-emerald-300 transition-all">
                      <ToggleLeft className="h-5 w-5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

