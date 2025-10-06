from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS, ALLOW_VERCEL_PREVIEWS_REGEX

def add_cors(app):
    """
    CORS simplificado e funcional
    """
    origins = ALLOWED_ORIGINS.copy() if ALLOWED_ORIGINS else ["*"]
    
    # Remover duplicatas
    origins = list(set(origins))
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print(f"✅ CORS configurado para todas as origens")