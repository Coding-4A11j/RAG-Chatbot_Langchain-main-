from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import get_settings
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/meta", tags=["meta"])


class MetaResponse(BaseModel):
    app_name: str
    environment: str
    api_version: str


@router.get("", response_model=ApiResponse[MetaResponse])
def metadata() -> ApiResponse[MetaResponse]:
    settings = get_settings()
    return ApiResponse(
        success=True,
        data=MetaResponse(
            app_name=settings.app_name,
            environment=settings.app_env,
            api_version="v1",
        ),
    )
