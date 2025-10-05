import os
from typing import List

API_NAME = "NebulaX API"
API_VERSION = "0.1.0"

# origens permitidas (dev + opcional FRONTEND_URL em produção)
ALLOWED_ORIGINS: List[str] = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://127.0.0.1:3000",
]

# habilita aceitar previews do Vercel (*.vercel.app) via regex
# deixe "1" enquanto estiver sem domínio final; depois pode trocar para "0"
ALLOW_VERCEL_PREVIEWS_REGEX = os.getenv("ALLOW_VERCEL_PREVIEWS_REGEX", "1") == "1"
