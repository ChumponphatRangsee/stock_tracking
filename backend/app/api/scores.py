from fastapi import APIRouter, HTTPException
from typing import List
from app.models.score import ScoreResponse
from app.database import supabase

router = APIRouter()

@router.get("/", response_model=List[ScoreResponse])
def get_all_scores():
    """Retrieve scores for all tracked stocks."""
    if not supabase: return []
    resp = supabase.table("stock_scores").select("*").execute()
    return resp.data

@router.get("/top", response_model=List[ScoreResponse])
def get_top_opportunities(limit: int = 20):
    """Retrieve the top opportunities based on opportunity_score."""
    if not supabase: return []
    resp = supabase.table("stock_scores").select("*").order("opportunity_score", desc=True).limit(limit).execute()
    return resp.data

@router.get("/{ticker}", response_model=ScoreResponse)
def get_stock_score(ticker: str):
    """Retrieve score for a specific stock."""
    if not supabase: return {}
    resp = supabase.table("stock_scores").select("*").eq("ticker", ticker).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Score not found")
    return resp.data[0]
