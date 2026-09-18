from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    model_mode: str
    model_loaded: bool

@router.get("/", response_model=HealthResponse, summary="Health Check")
async def health_check():
    from app.services.ml_service import ml_model
    from app.core.config import settings
    
    return HealthResponse(
        status="healthy",
        model_mode=settings.model_mode,
        model_loaded=ml_model.is_loaded
    )
