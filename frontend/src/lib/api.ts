import axios from 'axios';

const client = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

export const api = {
  // Stocks
  getStocks: (sector?: string) => client.get('/stocks/', { params: { sector } }).then(res => res.data),
  getStock: (ticker: string) => client.get(`/stocks/${ticker}`).then(res => res.data),
  
  // Scores
  getLatestScores: () => client.get('/scores/latest').then(res => res.data),
  getTopOpportunities: (limit = 20) => client.get(`/scores/top?limit=${limit}`).then(res => res.data),
  getScoreHistory: (ticker: string) => client.get(`/scores/${ticker}/history`).then(res => res.data),
  
  // Sectors
  getSectorRankings: () => client.get('/sectors/ranking').then(res => res.data),
  
  // Watchlist
  getWatchlist: () => client.get('/watchlist/').then(res => res.data),
  addToWatchlist: (ticker: string, note?: string) => client.post('/watchlist/', { ticker, note }).then(res => res.data),
  removeFromWatchlist: (ticker: string) => client.delete(`/watchlist/${ticker}`).then(res => res.data),
  
  // Manual trigger
  triggerRefresh: (ticker: string) => client.post(`/refresh/${ticker}`).then(res => res.data)
};
