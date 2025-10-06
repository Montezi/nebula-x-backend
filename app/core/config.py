import os
from typing import List

API_NAME = "NebulaX API"
API_VERSION = "0.1.0"

# ✅ GARANTIR todas as possíveis origens do frontend
ALLOWED_ORIGINS: List[str] = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://127.0.0.1:3000",
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://nebula-x-frontend.vercel.app",
    "https://*.vercel.app",
]

# ✅ REMOVER duplicatas
ALLOWED_ORIGINS = list(set(ALLOWED_ORIGINS))

ALLOW_VERCEL_PREVIEWS_REGEX = os.getenv("ALLOW_VERCEL_PREVIEWS_REGEX", "1") == "1"

