import random
from typing import List, Optional
import logging
from ..schemas.exoplanet import Exoplanet, Mission, Status
from .nasa_api import nasa_service
from .data_processor import NASADataProcessor
from .ml_service import ml_service

logger = logging.getLogger(__name__)

# “banco” em memória para o mock
_DB: List[Exoplanet] = []
_USE_REAL_DATA = False

def _generate_mock_with_k2(n=500) -> List[Exoplanet]:
    """Gera dados mock incluindo K2 de forma balanceada"""
    missions = ["Kepler", "K2", "TESS"]
    methods = ["Transit", "Radial Velocity", "Microlensing"]
    statuses = ["Confirmed", "Candidate", "False Positive"]
    
    data: List[Exoplanet] = []
    for i in range(n):
        mission = random.choice(missions)
        
        if mission == "K2":
            name = f"K2-{random.randint(100, 300)}"
            discovery_year = random.randint(2014, 2018)
        elif mission == "Kepler":
            name = f"Kepler-{random.randint(1000, 9999)}"
            discovery_year = random.randint(2009, 2013)
        else:  # TESS
            name = f"TOI-{random.randint(1000, 2000)}"
            discovery_year = random.randint(2018, 2023)
            
        data.append(Exoplanet(
            name=name,
            period=round(random.uniform(0.5, 500), 2),
            radius=round(random.uniform(0.5, 20), 2),
            temperature=random.randint(200, 2200),
            method=random.choice(methods),
            status=random.choice(statuses),
            mission=mission,
            discovery_year=discovery_year,
            habitable_zone=random.random() > 0.8,
            # prediction e confidence ficam como None inicialmente
        ))
    
    logger.info(f"🎯 Gerados {len(data)} planetas mock")
    return data

def _add_ml_predictions():
    """Adiciona predições ML aos dados existentes"""
    global _DB
    
    if not _DB or not ml_service.is_trained:
        return
    
    try:
        logger.info("🤖 Aplicando predições ML aos dados...")
        updated_db = []
        
        for planet in _DB:
            # Prepara dados para predição
            planet_data = {
                'period': planet.period,
                'radius': planet.radius,
                'temperature': planet.temperature,
                'discovery_year': planet.discovery_year,
                'habitable_zone': planet.habitable_zone,
                'confidence': 0.5  # Valor padrão
            }
            
            # Faz predição
            prediction_result = ml_service.predict(planet_data)
            
            # ✅ CORREÇÃO: Cria novo objeto sem os campos problemáticos
            planet_dict = planet.dict()
            # Remove os campos que vamos sobrescrever
            planet_dict.pop('prediction', None)
            planet_dict.pop('confidence', None)
            
            # Cria novo planeta com as predições
            updated_planet = Exoplanet(
                **planet_dict,
                prediction=prediction_result['prediction'],
                confidence=prediction_result['confidence']
            )
            updated_db.append(updated_planet)
        
        _DB = updated_db
        logger.info(f"✅ Predições ML aplicadas a {len(_DB)} planetas")
        
    except Exception as e:
        logger.error(f"❌ Erro ao aplicar predições ML: {str(e)}")

# ✅ INICIALIZAÇÃO IMEDIATA
def _initialize_db():
    global _DB
    if not _DB:
        _DB = _generate_mock_with_k2(500)
        logger.info(f"✅ Banco inicializado com {len(_DB)} planetas")
        
        # ✅ TREINA O MODELO AUTOMATICAMENTE
        try:
            logger.info("🤖 Treinando modelo ML automaticamente...")
            ml_result = ml_service.train_model(_DB)
            
            if ml_result["status"] == "success":
                logger.info(f"✅ Modelo ML treinado com acurácia: {ml_result['accuracy']}")
                # ✅ APLICA PREDIÇÕES AOS DADOS
                _add_ml_predictions()
            else:
                logger.error(f"❌ Falha no treinamento ML: {ml_result.get('error', 'Unknown error')}")
            
        except Exception as e:
            logger.error(f"❌ Erro no treinamento automático ML: {str(e)}")

# Chama a inicialização quando o módulo é importado
_initialize_db()

async def init_db(use_real_data: bool = False):
    """Inicializa/reinicializa o banco"""
    global _DB, _USE_REAL_DATA
    _USE_REAL_DATA = use_real_data
    
    logger.info("🔄 Inicializando banco de dados...")
    _DB = _generate_mock_with_k2(500)
    logger.info(f"✅ Banco (re)inicializado com {len(_DB)} dados mock")
    
    # ✅ TREINA NOVAMENTE AO REINICIALIZAR
    try:
        ml_result = ml_service.train_model(_DB)
        if ml_result["status"] == "success":
            _add_ml_predictions()
    except Exception as e:
        logger.error(f"❌ Erro no treinamento ML: {str(e)}")

def list_exoplanets(
    mission: Optional[Mission] = None,
    status: Optional[Status] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Exoplanet]:
    try:
        if not _DB:
            logger.warning("⚠️ _DB vazio, reinicializando...")
            _initialize_db()
        
        items = _DB.copy()
        
        if mission:
            items = [p for p in items if p.mission == mission]
        
        if status:
            items = [p for p in items if p.status == status]
        
        start_idx = min(offset, len(items))
        end_idx = min(offset + limit, len(items))
        result = items[start_idx:end_idx]
        
        # ✅ LOG COM INFO DE PREDIÇÕES
        predictions_count = len([p for p in result if p.prediction is not None])
        total_count = len(result)
        logger.info(f"📊 Retornando {total_count} planetas ({predictions_count} com predições)")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Erro em list_exoplanets: {str(e)}")
        fallback_data = _generate_mock_with_k2(10)
        return fallback_data

async def refresh(use_nasa: bool = False) -> List[Exoplanet]:
    """Atualiza dados - pode usar NASA API ou mock"""
    global _DB
    
    try:
        logger.info("🔄 Atualizando dados...")
        _DB = _generate_mock_with_k2(500)
        
        # ✅ TREINA NOVAMENTE AO ATUALIZAR
        ml_result = ml_service.train_model(_DB)
        if ml_result["status"] == "success":
            _add_ml_predictions()
            logger.info(f"✅ Dados atualizados: {len(_DB)} registros com predições ML")
        else:
            logger.warning(f"⚠️ Dados atualizados sem predições ML: {ml_result.get('error')}")
        
        return _DB[:50] 
    except Exception as e:
        logger.error(f"❌ Erro no refresh: {str(e)}")
        return []  

async def train_ml_model() -> dict:
    """Treina o modelo ML com os dados atuais"""
    try:
        result = ml_service.train_model(_DB)
        # ✅ APLICA PREDIÇÕES APÓS TREINAR
        if result["status"] == "success":
            _add_ml_predictions()
        return result
    except Exception as e:
        logger.error(f"❌ Erro no treinamento ML: {str(e)}")
        return {"accuracy": 0.0, "training_samples": 0, "status": "error", "error": str(e)}

def predict_exoplanet(planet_data: dict) -> dict:
    """Faz predição para um exoplaneta"""
    try:
        return ml_service.predict(planet_data)
    except Exception as e:
        logger.error(f"❌ Erro na predição: {str(e)}")
        return {"prediction": "Candidate", "confidence": 0.5, "error": str(e)}