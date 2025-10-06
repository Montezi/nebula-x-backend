import aiohttp
import asyncio
from typing import List, Dict, Any
import logging
import json  # ✅ ADICIONE ESTA IMPORT

logger = logging.getLogger(__name__)

class NASAApiService:
    def __init__(self):
        self.base_url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
        self.endpoints = {
            "confirmed": "?table=exoplanets&format=json",
            "kepler": "?table=cumulative&format=json&where=koi_disposition!=''",
            "k2": "?table=k2planets&format=json",
            "tess": "?table=toi&format=json&where=tess_disposition like 'Candidate'"
        }
    
    async def fetch_nasa_data(self, endpoint_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            endpoint = self.endpoints.get(endpoint_type, self.endpoints["confirmed"])
            url = f"{self.base_url}{endpoint}&rows={limit}"
            
            logger.info(f"🛰️ Fetching NASA data from: {url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status != 200:
                        logger.error(f"NASA API error: {response.status}")
                        return []
                    
                    # ✅ CORREÇÃO: Lê como texto e converte manualmente para JSON
                    text_data = await response.text()
                    
                    # Tenta parsear como JSON
                    try:
                        data = json.loads(text_data)
                        logger.info(f"✅ NASA data received: {len(data)} records")
                        return data
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ JSON decode error: {str(e)}")
                        logger.error(f"First 500 chars of response: {text_data[:500]}")
                        return []
                    
        except Exception as e:
            logger.error(f"❌ NASA API error: {str(e)}")
            return []

nasa_service = NASAApiService()