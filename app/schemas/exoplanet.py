from typing import Literal, Optional
from pydantic import BaseModel

Mission = Literal["Kepler", "K2", "TESS"]
Status  = Literal["Confirmed", "Candidate", "False Positive"]

class Exoplanet(BaseModel):
    name: str
    period: float
    radius: float
    temperature: int
    method: str
    status: Status
    mission: Mission
    discovery_year: int
    habitable_zone: bool
    prediction: Optional[Status] = None
    confidence: Optional[float] = None
