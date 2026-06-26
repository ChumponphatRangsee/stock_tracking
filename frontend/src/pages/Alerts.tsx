
import React, { useState, useEffect } from 'react';
import { Badge } from '../components/Badge';

import { PlusCircle, ToggleLeft, ToggleRight, Trash2, X } from 'lucide-react';
import { api } from '../lib/api';

export const Alerts: React.FC = () => {
































































  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  // Form states
  const [ticker, setTicker] = useState<string>("");
  const [metric, setMetric] = useState<string>("price");
  const [condition, setCondition] = useState<string>("less_than");
  const [valueThreshold, setValueThreshold] = useState<string>("");

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const data = await api.getAlerts();
      setAlerts(data);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticker.trim() || !valueThreshold.trim()) return;

    try {
      await api.createAlert({
        ticker: ticker.trim().toUpperCase(),
        metric,
        condition,
        value_threshold: parseFloat(valueThreshold),
      });
      setShowModal(false);
      setTicker("");
      setValueThreshold("");
      fetchAlerts();
    } catch (err) {
      console.error("Failed to create alert rule:", err);
      alert("Make sure ticker exists in monitored universe.");
    }
  };

  const handleToggle = async (id: number) => {
    try {
      await api.toggleAlert(id);
      fetchAlerts();
    } catch (err) {
      console.error("Failed to toggle alert rule:", err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteAlert(id);
      fetchAlerts();
    } catch (err) {
      console.error("Failed to delete alert rule:", err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">ALERTS MANAGER</h1>
          <span className="text-xs text-textSecondary font-medium">Configure cockpit triggers</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowModal(true)}
            className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold text-xs px-4 py-2 rounded-lg transition-all flex items-center gap-2"
          >
            <PlusCircle className="h-3.5 w-3.5" />
            Create Alert
          </button>
        </div>
      </div>

      {/* Main Alerts Table */}
      <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5">
        <div className="overflow-x-auto">
          {loading ? (
            <div className="h-48 flex items-center justify-center">
              <span className="text-xs text-textSecondary animate-pulse">Loading active alerts...</span>
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                  <th className="pb-3">Ticker</th>
                  <th className="pb-3">Alert Condition</th>
                  <th className="pb-3 text-right">Target Level</th>
                  <th className="pb-3 text-center">Status</th>
                  <th className="pb-3 text-center">Last Triggered</th>
                  <th className="pb-3 text-center">Toggle</th>
                  <th className="pb-3 text-center">Delete</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-6 text-center text-textSecondary text-xs">
                      No custom alert rules configured yet. Click "Create Alert" above to set up your first triggers!
                    </td>
                  </tr>
                ) : (
                  alerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-darkCardHover/40 transition-all">
                      <td className="py-3.5 text-emerald-400 font-bold">{alert.ticker}</td>
                      <td className="py-3.5 text-white capitalize">
                        {alert.metric.replace(/_/g, ' ')} {alert.condition === 'less_than' ? '<' : '>'}
                      </td>
                      <td className="py-3.5 text-right text-white font-bold">{alert.value_threshold.toFixed(2)}</td>
                      <td className="py-3.5 text-center">
                        <Badge type={alert.is_active ? "info" : "danger"}>
                          {alert.is_active ? "Active" : "Disabled"}
                        </Badge>
                      </td>
                      <td className="py-3.5 text-center text-textSecondary">
                        {alert.last_triggered_at ? new Date(alert.last_triggered_at).toLocaleString() : "-"}
                      </td>
                      <td className="py-3.5 text-center">
                        <button
                          onClick={() => handleToggle(alert.id)}
                          className="text-emerald-400 hover:text-emerald-300 transition-all"
                        >
                          {alert.is_active ? (
                            <ToggleRight className="h-6 w-6 inline text-emerald-500" />
                          ) : (
                            <ToggleLeft className="h-6 w-6 inline text-textSecondary" />
                          )}
                        </button>
                      </td>
                      <td className="py-3.5 text-center">
                        <button
                          onClick={() => handleDelete(alert.id)}
                          className="text-textSecondary hover:text-rose-400 transition-all"
                        >
                          <Trash2 className="h-4 w-4 inline" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Modal dialog for creating alert */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl max-w-md w-full p-6 space-y-6">
            <div className="flex justify-between items-center">
              <span className="text-lg font-bold text-white">Create Custom Alert</span>
              <button
                onClick={() => setShowModal(false)}
                className="text-textSecondary hover:text-white transition-all"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleCreateAlert} className="space-y-4">
              <div className="space-y-1">
                <label className="text-xs font-bold text-textSecondary uppercase tracking-wider block">Symbol Ticker</label>
                <input
                  type="text"
                  placeholder="e.g. MSFT"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  className="bg-darkBg border border-[#1F2937] text-white text-sm rounded p-2.5 w-full focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-textSecondary uppercase tracking-wider block">Metric</label>
                  <select
                    value={metric}
                    onChange={(e) => setMetric(e.target.value)}
                    className="bg-darkBg border border-[#1F2937] text-white text-sm rounded p-2.5 w-full focus:outline-none focus:border-emerald-500"
                  >
                    <option value="price">Stock Price</option>
                    <option value="pe_ratio">P/E Ratio</option>
                    <option value="margin_of_safety_pct">Margin of Safety %</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-textSecondary uppercase tracking-wider block">Condition</label>
                  <select
                    value={condition}
                    onChange={(e) => setCondition(e.target.value)}
                    className="bg-darkBg border border-[#1F2937] text-white text-sm rounded p-2.5 w-full focus:outline-none focus:border-emerald-500"
                  >
                    <option value="less_than">Falls Below (&lt;)</option>
                    <option value="greater_than">Spikes Above (&gt;)</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-textSecondary uppercase tracking-wider block">Target Value Threshold</label>
                <input
                  type="number"
                  step="any"
                  placeholder="e.g. 350.50 or 25"
                  value={valueThreshold}
                  onChange={(e) => setValueThreshold(e.target.value)}
                  className="bg-darkBg border border-[#1F2937] text-white text-sm rounded p-2.5 w-full focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm py-2.5 rounded-lg transition-all"
              >
                Save Trigger
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};