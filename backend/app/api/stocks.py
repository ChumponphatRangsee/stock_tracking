from fastapi import APIRouter
from typing import List
from app.models.stock import StockResponse
from app.database import supabase

router = APIRouter()

@router.get("/", response_model=List[StockResponse])
def get_stocks():
    """
    Retrieve all stocks in the universe.
    """
    if supabase is None:
        return []
    
    response = supabase.table("stocks").select("*").execute()
    return response.data

@router.get("/{ticker}", response_model=StockResponse)
def get_stock(ticker: str):
    """
    Retrieve a specific stock by ticker.
    """
    if supabase is None:
        return {"ticker": ticker, "company_name": "Test"}
    
    response = supabase.table("stocks").select("*").eq("ticker", ticker).execute()
    if response.data:
        return response.data[0]
    return {}
