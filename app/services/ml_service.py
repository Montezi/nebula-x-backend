import numpy as np
from typing import List, Tuple, Dict, Any
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.model_path = "models/exoplanet_model.pkl"
        self.accuracy = 0.0
        
    def extract_features(self, exoplanets: List[Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Extrai features dos exoplanetas para treinamento"""
        features = []
        labels = []
        
        for planet in exoplanets:
            try:
                # 6 features principais como discutido
                feature_vector = [
                    planet.period,
                    planet.radius,
                    planet.temperature,
                    planet.discovery_year,
                    1.0 if planet.habitable_zone else 0.0,
                    planet.confidence or 0.5
                ]
                
                # Label encoding
                status_map = {"Confirmed": 0, "Candidate": 1, "False Positive": 2}
                label = status_map.get(planet.status, 1)
                
                if all(x is not None for x in feature_vector):
                    features.append(feature_vector)
                    labels.append(label)
                    
            except Exception as e:
                continue
                
        return np.array(features), np.array(labels)
    
    def train_model(self, exoplanets: List[Any]) -> Dict[str, Any]:
        """Treina o modelo com dados de exoplanetas"""
        try:
            features, labels = self.extract_features(exoplanets)
            
            if len(features) < 10:
                raise ValueError("Dados insuficientes para treinamento")
            
            # Split dos dados
            X_train, X_test, y_train, y_test = train_test_split(
                features, labels, test_size=0.2, random_state=42
            )
            
            # Treina Random Forest
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            self.model.fit(X_train, y_train)
            
            # Avaliação
            y_pred = self.model.predict(X_test)
            self.accuracy = accuracy_score(y_test, y_pred)
            self.is_trained = True
            
            # Salva o modelo
            os.makedirs("models", exist_ok=True)
            joblib.dump(self.model, self.model_path)
            
            logger.info(f"✅ Modelo treinado com {len(features)} amostras. Acurácia: {self.accuracy:.3f}")
            
            return {
                "accuracy": round(self.accuracy, 3),
                "training_samples": len(features),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no treinamento: {str(e)}")
            return {
                "accuracy": 0.0,
                "training_samples": 0,
                "status": "error",
                "error": str(e)
            }
    
    def predict(self, planet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Faz predição para um novo exoplaneta"""
        if not self.is_trained or self.model is None:
            raise ValueError("Modelo não treinado")
        
        try:
            # Prepara features
            features = np.array([[
                planet_data.get('period', 0),
                planet_data.get('radius', 0),
                planet_data.get('temperature', 300),
                planet_data.get('discovery_year', 2015),
                1.0 if planet_data.get('habitable_zone', False) else 0.0,
                planet_data.get('confidence', 0.5)
            ]])
            
            prediction = self.model.predict(features)[0]
            confidence = np.max(self.model.predict_proba(features)[0])
            
            status_map = {0: "Confirmed", 1: "Candidate", 2: "False Positive"}
            
            return {
                "prediction": status_map[prediction],
                "confidence": round(confidence, 3),
                "features_used": len(features[0])
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na predição: {str(e)}")
            raise

ml_service = MLService()