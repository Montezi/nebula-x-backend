from typing import List
from fastapi import APIRouter
from ..schemas.analysis import LightCurvePoint, LightCurveAnalysis, TrainResponse
from ..services.analysis import analyze_lightcurve, train_model

router = APIRouter()

@router.post("/analysis/train", response_model=TrainResponse)
def train(): return train_model()

@router.post("/analysis/lightcurve", response_model=LightCurveAnalysis)
def lightcurve(points: List[LightCurvePoint]):
    return analyze_lightcurve(points)
