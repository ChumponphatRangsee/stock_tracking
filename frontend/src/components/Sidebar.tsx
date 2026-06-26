import React from 'react';
import { 
  TrendingUp, 
  Eye, 
  Sliders, 
  Layers, 
  Bell, 
  Folder, 
  Settings as SettingsIcon,
  LogOut
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onViewChange }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
    { id: 'watchlist', label: 'Watchlist', icon: Eye },
    { id: 'screener', label: 'Screener', icon: Sliders },
    { id: 'detail', label: 'Stock Detail', icon: Layers },
    { id: 'alerts', label: 'Alerts', icon: Bell },
    { id: 'portfolio', label: 'Portfolio', icon: Folder },
    { id: 'settings', label: 'Settings', icon: SettingsIcon }
  ];

  return (
    <aside className="w-64 bg-darkCard border-r border-[#1F2937] flex flex-col h-screen sticky top-0">
      {/* Platform Title */}
      <div className="h-16 flex items-center px-6 border-b border-[#1F2937]">
        <span className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
          QUANTCOCKPIT
        </span>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-4 py-6 space-y-1.5">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                isActive 
                  ? 'bg-emerald-500/10 text-emerald-400 border-l-4 border-emerald-500 pl-3' 
                  : 'text-textSecondary hover:bg-darkCardHover hover:text-white border-l-4 border-transparent'
              }`}
            >
              <Icon className={`h-4 w-4 ${isActive ? 'text-emerald-400' : 'text-textSecondary'}`} />
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Footer / Info */}
      <div className="p-4 border-t border-[#1F2937]">
        <div className="flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium text-textSecondary hover:bg-[#ef4444]/10 hover:text-[#ef4444] cursor-pointer transition-all duration-150">
          <LogOut className="h-4 w-4" />
          <span>Exit Cockpit</span>
        </div>
      </div>
    </aside>
  );
};
