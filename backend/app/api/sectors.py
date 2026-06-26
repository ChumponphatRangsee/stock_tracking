from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

@router.get("/")
def get_sectors():
    """
    Retrieve average opportunity score by sector.
    """
    if not supabase: return []
    
    # We execute a raw SQL query using Supabase RPC if we set it up,
    # or we can just fetch all scores and stocks and group them here for MVP
    
    stocks_resp = supabase.table("stocks").select("ticker, sector").execute()
    scores_resp = supabase.table("stock_scores").select("ticker, opportunity_score").execute()
    
    if not stocks_resp.data or not scores_resp.data:
        return []
        
    sector_data = {}
    score_map = {item['ticker']: item['opportunity_score'] for item in scores_resp.data if item['opportunity_score']}
    
    for stock in stocks_resp.data:
        sector = stock.get("sector")
        ticker = stock.get("ticker")
        
        if not sector or ticker not in score_map:
            continue
            
        if sector not in sector_data:
            sector_data[sector] = []
            
        sector_data[sector].append(score_map[ticker])
        
    results = []
    for sector, scores in sector_data.items():
        avg_score = sum(scores) / len(scores)
        results.append({
            "sector": sector,
            "average_opportunity_score": round(avg_score, 2),
            "stock_count": len(scores)
        })
        
    return sorted(results, key=lambda x: x["average_opportunity_score"], reverse=True)
