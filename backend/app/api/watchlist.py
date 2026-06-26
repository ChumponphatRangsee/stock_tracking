from fastapi import APIRouter, HTTPException
from typing import List
from app.models.watchlist import WatchlistResponse, WatchlistCreate
from app.database import supabase

router = APIRouter()

@router.get("/", response_model=List[WatchlistResponse])
def get_watchlist():
    if not supabase: return []
    resp = supabase.table("watchlist").select("*").execute()
    return resp.data

@router.post("/", response_model=WatchlistResponse)
def add_to_watchlist(item: WatchlistCreate):
    if not supabase: raise HTTPException(status_code=500, detail="Database not configured")
    
    # Check if exists
    existing = supabase.table("watchlist").select("*").eq("ticker", item.ticker).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Ticker already in watchlist")
        
    resp = supabase.table("watchlist").insert({"ticker": item.ticker}).execute()
    return resp.data[0]

@router.delete("/{ticker}")
def remove_from_watchlist(ticker: str):
    if not supabase: raise HTTPException(status_code=500, detail="Database not configured")
    supabase.table("watchlist").delete().eq("ticker", ticker).execute()
    return {"message": f"{ticker} removed from watchlist"}
