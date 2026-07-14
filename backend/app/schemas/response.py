from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetails(BaseModel):
    code: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable error message")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetails] = None


class HealthResponse(BaseModel):
    status: str
    service: str
