# exceptions.py
from typing import Any


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


class HttpResponseError(AppExceptionError):
    """Exception raised for HTTP response errors."""

    default_message: str = "Error response from external service."
    status_code: int = 502


class HTTPConnectionError(AppExceptionError):
    """Exception raised for HTTP connection errors."""

    default_message: str = "Service unavailable: Failed to connect to external service."
    status_code: int = 503


class HTTPGenricError(AppExceptionError):
    """Generic HTTP exception."""

    default_message: str = "An unexpected HTTP error occurred."
    status_code: int = 500
