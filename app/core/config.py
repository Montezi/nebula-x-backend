import os
from typing import List

API_NAME = "NebulaX API"
API_VERSION = "0.1.0"

# porta/urls do frontend permitidos no dev
ALLOWED_ORIGINS: List[str] = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://127.0.0.1:3000",
]
