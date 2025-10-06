from fastapi import FastAPI
from .core.cors import add_cors
from .core import config
from .api import health, exoplanets, analysis

app = FastAPI(title=config.API_NAME, version=config.API_VERSION)

# CORS 
add_cors(app)

# ✅ INICIALIZAÇÃO 
@app.on_event("startup")
async def startup_event():
    from .services.exoplanets import init_db
    await init_db(use_real_data=False)

# Rotas
app.include_router(health.router)
app.include_router(exoplanets.router)
app.include_router(analysis.router)

