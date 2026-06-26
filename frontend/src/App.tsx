import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Watchlist } from './pages/Watchlist';
import { Screener } from './pages/Screener';
import { StockDetail } from './pages/StockDetail';
import { Alerts } from './pages/Alerts';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<string>('dashboard');
  const [selectedTicker, setSelectedTicker] = useState<string>('AAPL');

  const handleNavigateToStock = (ticker: string) => {
    setSelectedTicker(ticker);
    setCurrentView('detail');
  };

  return (
    <div className="flex bg-[#0B0F19] min-h-screen text-textPrimary">
      {/* Persistent Sidebar */}
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />

      {/* Main Area Wrapper */}
      <main className="flex-1 p-8 overflow-y-auto">
        {currentView === 'dashboard' && (
          <Dashboard onNavigateToStock={handleNavigateToStock} />
        )}
        {currentView === 'watchlist' && (
          <Watchlist />
        )}
        {currentView === 'screener' && (
          <Screener onNavigateToStock={handleNavigateToStock} />
        )}
        {currentView === 'detail' && (
          <StockDetail selectedTicker={selectedTicker} />
        )}
        {currentView === 'alerts' && (
          <Alerts />
        )}
        {currentView === 'portfolio' && (
          <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-2">
            <span className="text-lg font-bold text-white">PORTFOLIO TRACKER</span>
            <span className="text-sm text-textSecondary max-w-sm">Detailed personal cost-basis tracking is slated for V2 deployment. Mock status displays will sit here.</span>
          </div>
        )}
        {currentView === 'settings' && (
          <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-2">
            <span className="text-lg font-bold text-white">SYSTEM SETTINGS</span>
            <span className="text-sm text-textSecondary max-w-sm">Configuration of API schedules, webhook triggers, and database resets.</span>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;

