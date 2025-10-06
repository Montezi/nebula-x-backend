from typing import List, Optional
from fastapi import APIRouter, Query
from ..schemas.exoplanet import Exoplanet, Mission, Status
from ..services.exoplanets import list_exoplanets, refresh

router = APIRouter()

@router.get("/exoplanets", response_model=List[Exoplanet])
def get_exoplanets(
    mission: Optional[Mission] = Query(None), 
    status: Optional[Status] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return list_exoplanets(mission, status, limit, offset)

@router.get("/exoplanets/refresh", response_model=List[Exoplanet])
async def refresh_exoplanets():  
    return await refresh()  