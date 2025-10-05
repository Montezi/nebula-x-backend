from fastapi import FastAPI
from .core.cors import add_cors
from .core import config
from .api import health, exoplanets, analysis
from .services.exoplanets import init_db

app = FastAPI(title=config.API_NAME, version=config.API_VERSION)

add_cors(app)

# Inicializa mock (ou carregamento inicial)
init_db()

# monta as rotas
app.include_router(health.router)
app.include_router(exoplanets.router)
app.include_router(analysis.router)
