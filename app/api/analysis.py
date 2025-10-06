from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from ..schemas.analysis import LightCurvePoint, LightCurveAnalysis, TrainResponse
from ..services.analysis import analyze_lightcurve  # ✅ AGORA EXISTE
from ..services.exoplanets import train_ml_model, predict_exoplanet
from ..services.ml_service import ml_service

router = APIRouter()

@router.post("/analysis/train", response_model=TrainResponse)
async def train():
    """Treina com sistema ML real"""
    try:
        result = await train_ml_model()
        return TrainResponse(
            message="Modelo NASA treinado com sucesso",
            accuracy=result["accuracy"]
        )
    except Exception as e:
        raise HTTPException(500, detail=f"Erro no treinamento: {str(e)}")

@router.post("/analysis/lightcurve", response_model=LightCurveAnalysis)
def lightcurve(points: List[LightCurvePoint]):
    """Mantém análise simples de curva de luz"""
    return analyze_lightcurve(points)  # ✅ USA A FUNÇÃO DO SERVICE

@router.post("/analysis/predict")
async def predict_planet(planet_data: Dict[str, Any]):
    """Predição com ML real"""
    try:
        if ml_service.is_trained:
            return ml_service.predict(planet_data)
        else:
            return {"prediction": "Candidate", "confidence": 0.5, "status": "model_not_trained"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))