# exceptions.py
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger


class AppExceptionError(Exception):
    """Base exception for all clients."""

    default_message: str = "An application error occurred."
    status_code: int = 400
    context: dict[str, Any]

    def __init__(
        self,
        message: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        status_code: int | None = None,  # optional override
    ):
        self.message = message or self.default_message
        self.context = context or {}
        self.__cause__ = cause
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """JSON-friendly representation."""
        data: dict[str, Any] = {
            "error": self.__class__.__name__,
            "message": self.message,
        }
        if self.context:
            data["context"] = self.context.copy()
        if self.__cause__:
            data["cause"] = str(self.__cause__)
        return data


# register
async def global_exception_handler(request: Request, exc: AppExceptionError):  # noqa: RUF029
    """Dynamic response handler for AppExceptionError.

    - Default: JSON
    - Plain text: if header X-Response-Format=text or query param format=text
    """
    log_context = {
        "path": str(request.url.path),
        "method": request.method,
        "client": request.client.host if request.client else None,
        "status_code": exc.status_code,
        "context": exc.context,
        "cause": str(exc.__cause__) if exc.__cause__ else None,
    }
    logger.bind(**log_context).error(exc.message)
    response_format = request.headers.get(
        "X-Response-Format"
    ) or request.query_params.get("format", "json")

    if response_format.lower() == "text":
        text = f"[{exc.__class__.__name__}] {exc.message}"
        if exc.context:
            text += f" | context={exc.context}"
        if exc.__cause__:
            text += f" | cause={exc.__cause__}"
        return PlainTextResponse(text, status_code=exc.status_code)

    return JSONResponse(content=exc.to_dict(), status_code=exc.status_code)


class HttpResponseError(AppExceptionError):
    """Exception raised for HTTP response errors."""

    default_message: str = "Error response from external service."
    status_code: int = 502


# buat custom exception seterus nya ke bawah
class HTTPConnectionError(AppExceptionError):
    """Exception raised for HTTP connection errors."""

    default_message: str = "Service unavailable: Failed to connect to external service."
    status_code: int = 503


class HTTPGenricError(AppExceptionError):
    """Generic HTTP exception."""

    default_message: str = "An unexpected HTTP error occurred."
    status_code: int = 500
