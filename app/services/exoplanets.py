import random
from typing import List, Optional
from ..schemas.exoplanet import Exoplanet, Mission, Status

# “banco” em memória para o mock
_DB: List[Exoplanet] = []

def _generate_mock(n=150) -> List[Exoplanet]:
    missions = ["Kepler", "K2", "TESS"]
    methods  = ["Transit", "Radial Velocity", "Microlensing"]
    statuses = ["Confirmed", "Candidate", "False Positive"]
    data: List[Exoplanet] = []
    for _ in range(n):
        mission = random.choice(missions)
        data.append(Exoplanet(
            name=f"{mission}-{random.randint(1000,9999)}",
            period=round(random.uniform(0.5, 500), 2),
            radius=round(random.uniform(0.5, 20), 2),
            temperature=random.randint(200, 2200),
            method=random.choice(methods),
            status=random.choice(statuses),  # type: ignore
            mission=mission,                 # type: ignore
            discovery_year=random.randint(2009, 2022),
            habitable_zone=random.random() > 0.8,
        ))
    return data

def init_db():
    global _DB
    if not _DB:
        _DB = _generate_mock(150)

def list_exoplanets(
    mission: Optional[Mission] = None,
    status: Optional[Status] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Exoplanet]:
    init_db()
    items = _DB
    if mission:
        items = [p for p in items if p.mission == mission]
    if status:
        items = [p for p in items if p.status == status]
    return items[offset: offset + limit]

def refresh() -> List[Exoplanet]:
    """Simula atualização (depois aqui entra NASA API)."""
    global _DB
    _DB = _generate_mock(150)
    return _DB[:50]
