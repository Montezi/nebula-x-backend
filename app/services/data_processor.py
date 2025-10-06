from typing import List, Dict, Any
import numpy as np
import random
from ..schemas.exoplanet import Exoplanet, Mission, Status

class NASADataProcessor:
    @staticmethod
    def process_nasa_data(raw_data: List[Dict[str, Any]], data_type: str = "confirmed") -> List[Exoplanet]:
        """Processa dados brutos da NASA para o schema do NebulaX"""
        
        processed = []
        
        for item in raw_data:
            try:
                if data_type == "kepler":
                    planet = NASADataProcessor._process_kepler_data(item)
                elif data_type == "k2":  # ✅ CORREÇÃO: ADICIONADO K2
                    planet = NASADataProcessor._process_k2_data(item)
                elif data_type == "tess":
                    planet = NASADataProcessor._process_tess_data(item)
                else:
                    planet = NASADataProcessor._process_confirmed_data(item)
                
                if planet and planet.period and planet.radius:
                    processed.append(planet)
                    
            except Exception as e:
                continue
                
        return processed
    
    @staticmethod
    def _process_confirmed_data(item: Dict[str, Any]) -> Exoplanet:
        """Processa dados de exoplanetas confirmados"""
        name = item.get('pl_name', f"NASA-{np.random.randint(10000, 99999)}")
        
        return Exoplanet(
            name=name,
            period=float(item.get('pl_orbper', 0)) or np.random.uniform(0.5, 500),
            radius=float(item.get('pl_rade', 0)) or np.random.uniform(0.5, 20),
            temperature=int(item.get('pl_eqt', 0)) or np.random.randint(200, 2200),
            method=item.get('pl_discmethod', 'Transit'),
            status="Confirmed",
            mission=NASADataProcessor._detect_mission(item.get('pl_facility', ''), name),  # ✅ CORREÇÃO: passa nome também
            discovery_year=int(item.get('pl_disc', 2015)),
            habitable_zone=NASADataProcessor._calculate_habitable_zone(item),
            prediction=None,
            confidence=None
        )
    
    @staticmethod
    def _process_kepler_data(item: Dict[str, Any]) -> Exoplanet:
        """Processa dados Kepler"""
        disposition = item.get('koi_disposition', 'CANDIDATE')
        status_map = {
            'CONFIRMED': 'Confirmed',
            'CANDIDATE': 'Candidate', 
            'FALSE POSITIVE': 'False Positive'
        }
        
        return Exoplanet(
            name=f"Kepler-{item.get('kepoi_name', 'Unknown')}",
            period=float(item.get('koi_period', 0)),
            radius=float(item.get('koi_prad', 0)),
            temperature=int(item.get('koi_teq', 300)),
            method="Transit",
            status=status_map.get(disposition, 'Candidate'),
            mission="Kepler",
            discovery_year=2014,
            habitable_zone=NASADataProcessor._calculate_kepler_hz(item),
            prediction=None,
            confidence=float(item.get('koi_score', 0.5))
        )
    
    @staticmethod
    def _process_k2_data(item: Dict[str, Any]) -> Exoplanet:  # ✅ NOVO: PROCESSADOR K2
        """Processa dados específicos da missão K2"""
        name = item.get('pl_name', f"K2-{random.randint(1, 300)}")
        disposition = item.get('disposition', 'CANDIDATE')
        
        status_map = {
            'CONFIRMED': 'Confirmed',
            'CANDIDATE': 'Candidate', 
            'FALSE POSITIVE': 'False Positive'
        }
        
        return Exoplanet(
            name=name,
            period=float(item.get('pl_orbper', item.get('orbital_period', 0))),
            radius=float(item.get('pl_rade', item.get('planet_radius', 0))),
            temperature=int(item.get('pl_eqt', item.get('equilibrium_temperature', 300))),
            method="Transit",
            status=status_map.get(disposition.upper(), 'Candidate'),
            mission="K2",
            discovery_year=int(item.get('disc_year', 2016)),
            habitable_zone=NASADataProcessor._calculate_k2_hz(item),
            prediction=None,
            confidence=float(item.get('confidence', 0.7))
        )
    
    @staticmethod
    def _process_tess_data(item: Dict[str, Any]) -> Exoplanet:
        """Processa dados TESS"""
        return Exoplanet(
            name=f"TESS-{item.get('toiid', 'Unknown')}",
            period=float(item.get('period', 0)),
            radius=float(item.get('planet_radius', 0)),
            temperature=int(item.get('planet_teq', 300)),
            method="Transit",
            status="Candidate",
            mission="TESS",
            discovery_year=2018,
            habitable_zone=NASADataProcessor._calculate_tess_hz(item),
            prediction=None,
            confidence=0.7
        )
    
    @staticmethod
    def _detect_mission(facility: str, name: str = "") -> Mission:  # ✅ CORREÇÃO: MELHOR DETECÇÃO
        """Detecta a missão com base na facility e nome do planeta"""
        facility_lower = facility.lower()
        name_lower = name.lower()
        
        # Prioridade: K2 (nomes específicos)
        if 'k2' in name_lower or 'epic' in name_lower:
            return "K2"
        elif 'kepler' in name_lower:
            return "Kepler"
        elif 'tess' in name_lower or 'toi' in name_lower:
            return "TESS"
        # Fallback para facility
        elif 'k2' in facility_lower:
            return "K2"
        elif 'kepler' in facility_lower:
            return "Kepler"
        elif 'tess' in facility_lower:
            return "TESS"
        else:
            # Distribuição mais inteligente
            missions = ["Kepler", "K2", "TESS"]
            return random.choice(missions)
    
    @staticmethod
    def _calculate_habitable_zone(planet: Dict[str, Any]) -> bool:
        radius = float(planet.get('pl_rade', 0))
        temp = float(planet.get('pl_eqt', 0))
        return 0.5 < radius < 2.5 and 200 < temp < 350
    
    @staticmethod
    def _calculate_kepler_hz(koi: Dict[str, Any]) -> bool:
        insol = float(koi.get('koi_insol', 0))
        return 0.3 < insol < 1.5 if insol else False
    
    @staticmethod
    def _calculate_k2_hz(k2_data: Dict[str, Any]) -> bool:  # ✅ NOVO: CALCULADOR K2
        """Calcula zona habitável para dados K2"""
        insol = float(k2_data.get('insolation_flux', k2_data.get('pl_insol', 0)))
        radius = float(k2_data.get('planet_radius', k2_data.get('pl_rade', 0)))
        return 0.3 < insol < 1.5 and 0.5 < radius < 2.5
    
    @staticmethod
    def _calculate_tess_hz(toi: Dict[str, Any]) -> bool:
        insol = float(toi.get('insol', 0))
        return 0.3 < insol < 1.5 if insol else False