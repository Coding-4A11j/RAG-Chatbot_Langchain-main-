from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.response import ApiResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=ApiResponse[HealthResponse])
def liveness() -> ApiResponse[HealthResponse]:
    settings = get_settings()
    return ApiResponse(success=True, data=HealthResponse(status="ok", service=settings.app_name))


@router.get("/ready", response_model=ApiResponse[HealthResponse])
def readiness() -> ApiResponse[HealthResponse]:
    settings = get_settings()
    return ApiResponse(success=True, data=HealthResponse(status="ready", service=settings.app_name))
