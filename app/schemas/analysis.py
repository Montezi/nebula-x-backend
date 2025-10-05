from pydantic import BaseModel
from typing import List

class TrainResponse(BaseModel):
    message: str
    accuracy: float

class LightCurvePoint(BaseModel):
    time: float
    flux: float

class LightCurveAnalysis(BaseModel):
    transits: int
    confidence: float
