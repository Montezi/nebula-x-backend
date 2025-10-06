from typing import List
from ..schemas.analysis import LightCurvePoint, LightCurveAnalysis

def analyze_lightcurve(points: List[LightCurvePoint]) -> LightCurveAnalysis:
    """Análise simplificada de curva de luz para demonstração"""
    if not points or len(points) < 10:
        return LightCurveAnalysis(transits=0, confidence=0.0)
    
    # Lógica simplificada para demo
    fluxes = [p.flux for p in points]
    mean_flux = sum(fluxes) / len(fluxes)
    variance = sum((f - mean_flux) ** 2 for f in fluxes) / len(fluxes)
    
    # Calcula confiança baseada na variância
    confidence = max(0.3, 0.9 - (variance * 5))
    
    # Detecta trânsitos baseado em picos de variância
    transits = 1 if variance > 0.001 else 0
    
    return LightCurveAnalysis(
        transits=transits, 
        confidence=round(confidence, 2)
    )