import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  change?: number; // Positive/Negative percentage
  icon?: React.ComponentType<any>;
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, subValue, change, icon: Icon }) => {
  const isPositive = change && change > 0;
  
  return (
    <div className="bg-[#111827] border border-[#1F2937] p-5 rounded-lg flex flex-col justify-between transition-all duration-150 hover:border-[#374151]">
      <div className="flex justify-between items-start">
        <span className="text-xs font-semibold tracking-wider text-textSecondary uppercase">{title}</span>
        {Icon && <Icon className="h-4 w-4 text-textSecondary" />}
      </div>
      
      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {change !== undefined && (
          <span className={`text-xs font-semibold px-1.5 py-0.5 rounded ${
            isPositive ? 'text-emerald-400 bg-emerald-500/10' : 'text-rose-400 bg-rose-500/10'
          }`}>
            {isPositive ? '+' : ''}{change}%
          </span>
        )}
      </div>

      {subValue && (
        <span className="mt-1 text-xs text-textSecondary font-medium">{subValue}</span>
      )}
    </div>
  );
};
