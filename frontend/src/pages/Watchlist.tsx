import React, { useState, useEffect } from 'react';
import { PlusCircle, Trash2 } from 'lucide-react';
import { api } from '../lib/api';

export const Watchlist: React.FC = () => {
  const [watchlistItems, setWatchlistItems] = useState<any[]>([]);
  const [newTicker, setNewTicker] = useState<string>("");
  const [newNote, setNewNote] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchWatchlist();
  }, []);

  const fetchWatchlist = async () => {
    try {
      const items = await api.getWatchlist();
      setWatchlistItems(items);
    } catch (err) {
      console.error("Failed to fetch watchlist:", err);
    }
  };

  const handleAddTicker = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTicker.trim()) return;
    setLoading(true);
    try {
      // 1. Trigger background refresh on the backend for the stock to guarantee it exists and has metrics computed
      await api.triggerRefresh(newTicker.trim().toUpperCase());
      
      // 2. Add to Watchlist table
      await api.addToWatchlist(newTicker.trim().toUpperCase(), newNote.trim() || undefined);
      
      setNewTicker("");
      setNewNote("");
      fetchWatchlist();
    } catch (err) {
      console.error("Error adding to watchlist:", err);
      alert("Make sure ticker exists and database is connected.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTicker = async (ticker: string) => {
    try {
      await api.removeFromWatchlist(ticker);
      fetchWatchlist();
    } catch (err) {
      console.error("Error removing from watchlist:", err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Row */}
      <div className="flex justify-between items-center h-12">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white m-0">WATCHLIST CONTROLLER</h1>
          <span className="text-xs text-textSecondary font-medium">Your curated monitor list</span>
        </div>
      </div>

      {/* Add Ticker Mini-Form Panel */}
      <form onSubmit={handleAddTicker} className="bg-darkCard border border-[#1F2937] p-4 rounded-lg flex items-end gap-4 max-w-2xl">
        <div className="flex-1 space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Symbol Ticker</label>
          <input
            type="text"
            placeholder="e.g. MSFT"
            value={newTicker}
            onChange={(e) => setNewTicker(e.target.value)}
            className="bg-[#111827] border border-[#1F2937] text-white text-sm rounded p-2 w-full focus:outline-none focus:border-emerald-500"
          />
        </div>
        <div className="flex-1 space-y-1">
          <label className="text-[10px] font-bold text-textSecondary uppercase tracking-wider block">Custom Note</label>
          <input
            type="text"
            placeholder="Optional rationale..."
            value={newNote}
            onChange={(e) => setNewNote(e.target.value)}
            className="bg-[#111827] border border-[#1F2937] text-white text-sm rounded p-2 w-full focus:outline-none focus:border-emerald-500"
          />
        </div>
        <button 
          type="submit" 
          disabled={loading}
          className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white font-semibold text-xs px-5 py-2.5 rounded-lg transition-all flex items-center gap-2 h-10"
        >
          <PlusCircle className="h-4 w-4" />
          {loading ? 'Adding...' : 'Add Stock'}
        </button>
      </form>

      {/* Main Table Card */}
      <div className="bg-darkCard border border-[#1F2937] rounded-lg p-5">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#1F2937] text-textSecondary text-xs font-semibold uppercase tracking-wider">
                <th className="pb-3">Ticker</th>
                <th className="pb-3">Company</th>
                <th className="pb-3">Personal Note</th>
                <th className="pb-3 text-center">Added At</th>
                <th className="pb-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1f2937]/50 text-sm font-medium">
              {watchlistItems.length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-6 text-center text-textSecondary text-xs">
                    Your Watchlist is empty. Enter a ticker above to start monitoring!
                  </td>
                </tr>
              ) : (
                watchlistItems.map((item) => (
                  <tr key={item.id} className="hover:bg-darkCardHover/40 transition-all">
                    <td className="py-3.5 text-emerald-400 font-bold">{item.ticker}</td>
                    <td className="py-3.5 text-white max-w-xs truncate">{item.company_name || 'Processing...'}</td>
                    <td className="py-3.5 text-textSecondary italic">{item.note || 'No notes added'}</td>
                    <td className="py-3.5 text-center text-textSecondary">{new Date(item.created_at).toLocaleDateString()}</td>
                    <td className="py-3.5 text-center">
                      <button 
                        onClick={() => handleDeleteTicker(item.ticker)}
                        className="text-textSecondary hover:text-rose-400 p-1 transition-all"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

