from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS, ALLOW_VERCEL_PREVIEWS_REGEX

def add_cors(app):
    """
    Aplica CORS ao FastAPI. Use ALLOWED_ORIGINS para origens fixas (localhost / FRONTEND_URL)
    e, opcionalmente, allow_origin_regex para previews do Vercel (*.vercel.app).
    """
    kwargs = {
        "allow_origins": ALLOWED_ORIGINS.copy(),
        "allow_credentials": False,      # mude para True apenas se usar cookies/credenciais
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }

    # aceita qualquer subdomínio do Vercel (previews): https://*.vercel.app
    if ALLOW_VERCEL_PREVIEWS_REGEX:
        kwargs["allow_origin_regex"] = r"https://.*\.vercel\.app"

    app.add_middleware(CORSMiddleware, **kwargs)
