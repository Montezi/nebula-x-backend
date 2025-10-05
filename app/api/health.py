from fastapi import APIRouter
from ..core.config import API_NAME, API_VERSION

router = APIRouter()

@router.get("/health")
def health(): return {"ok": True}

@router.get("/version")
def version(): return {"name": API_NAME, "version": API_VERSION}
