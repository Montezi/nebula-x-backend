import time
from typing import List
from ..schemas.analysis import LightCurvePoint, TrainResponse, LightCurveAnalysis

def train_model() -> TrainResponse:
    time.sleep(0.25)  # simula tempo de treino
    import random
    acc = round(random.uniform(0.7, 0.95), 2)
    return TrainResponse(message="Modelo treinado com sucesso", accuracy=acc)

def analyze_lightcurve(points: List[LightCurvePoint]) -> LightCurveAnalysis:
    if not points:
        return LightCurveAnalysis(transits=0, confidence=0.0)
    values = [p.flux for p in points]
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    conf = max(0.6, min(0.95, 1.0 - min(var, 1.0) * 0.2))
    transits = 1 if var > 0.005 else 0
    return LightCurveAnalysis(transits=transits, confidence=round(conf, 2))
