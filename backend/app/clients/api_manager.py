import httpx
from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import APIQuotaExceededError, APIProviderError
from app.services.quota_service import QuotaService
from app.models.raw_api_response import RawApiResponse
import hashlib
import json

class ApiManager:
    """
    The master class for handling external HTTP requests.
    It checks quotas, executes the HTTP request, and saves the RAW JSON to the database.
    """
    def __init__(self, db: Session):
        self.db = db

    async def execute_request(self, provider: str, ticker: str, url: str) -> Optional[dict]:
        """
        1. Check Quota
        2. Make HTTP Call
        3. Save Raw JSON to DB
        """
        # Step 1: Check Quota
        if not QuotaService.can_make_request(self.db, provider):
            raise APIQuotaExceededError(provider, f"Daily limit reached for {provider}")

        # Step 2: Execute Request
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                
            if response.status_code == 429:
                raise APIProviderError(f"Rate limited (429) by {provider}")
                
            response.raise_for_status()
            data = response.json()
            
            # Step 3: Log usage and save raw data
            QuotaService.increment_quota(self.db, provider)
            self._save_raw_response(provider, ticker, url, data)
            
            return data

        except httpx.HTTPStatusError as e:
            raise APIProviderError(f"HTTP Error {e.response.status_code} from {provider} on URL: {url.split('?')[0]}")
        except Exception as e:
            raise APIProviderError(f"Connection error: {str(e)}")

    def _save_raw_response(self, provider: str, ticker: str, endpoint: str, data: dict):
        """Hashes the JSON and saves it so we can check for deltas later."""
        clean_endpoint = endpoint.split("?")[0]
        
        json_str = json.dumps(data, sort_keys=True)
        response_hash = hashlib.md5(json_str.encode()).hexdigest()
        
        raw_resp = RawApiResponse(
            provider=provider,
            ticker=ticker,
            endpoint=clean_endpoint,
            response_hash=response_hash,
            response_json=data
        )
        self.db.add(raw_resp)
        self.db.commit()
