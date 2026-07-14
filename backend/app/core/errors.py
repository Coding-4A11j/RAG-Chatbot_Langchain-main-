from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


class ApiException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(status_code=status_code, detail={"code": code, "message": message})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiException)
    async def handle_api_exception(_: Request, exc: ApiException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": exc.detail.get("code", "API_ERROR"),
                    "message": exc.detail.get("message", "Request failed"),
                },
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                },
            },
        )
