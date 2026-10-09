from fastapi import APIRouter
from ...config import settings
from ...services.gemma_provider import gemma_service
from ...services.gmail_service import gmail_service

router = APIRouter()

@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_engine": gemma_service.get_status()["provider"],
        "gmail_integration": gmail_service.get_status().message
    }
