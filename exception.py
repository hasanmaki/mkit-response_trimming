"""custom application exceptions."""


class AppExceptionError(Exception):
    """Base exception with adapter support."""

    default_message: str = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
        name: str = "AppExceptionError",
        context: dict | None = None,
        cause: Exception | None = None,
    ):
        self.message = message or self.default_message
        self.name = name
        self.context = context or {}
        self.__cause__ = cause
        super().__init__(self.message)

    def __str__(self):
        base = f"[HTTP Error] {self.message}"
        ctx = f" | context={self.context}" if self.context else ""
        cause = f" | cause={self.__cause__}" if self.__cause__ else ""
        return base + ctx + cause


class HTTPGenericError(AppExceptionError):
    """Base exception for all HTTP-related errors."""

    default_message: str = "An HTTP error occurred."
    status_code: int = 500
    response_type: str = "json"

    def __init__(
        self,
        message: str | None = None,
        name: str = "HTTPGenericError",
        context: dict | None = None,
        cause: Exception | None = None,
        status_code: int | None = None,
        response_type: str | None = None,
    ):
        super().__init__(message, name, context, cause)
        if status_code is not None:
            self.status_code = status_code
        if response_type is not None:
            self.response_type = response_type


class HTTPConnectionError(HTTPGenericError):
    """Exception raised for HTTP connection errors."""

    default_message: str = "Service unavailable: Failed to connect to external service."
    status_code: int = 503
    response_type: str = "json"


class HttpResponseError(HTTPGenericError):
    """Exception raised for HTTP response errors."""

    default_message: str = "Error response from external service."
    status_code: int = 502
    response_type: str = "json"


class HttpMethodeNotAllowedError(HTTPGenericError):
    """Exception raised for HTTP method not allowed errors."""

    default_message: str = "HTTP method not allowed."
    status_code: int = 405
    response_type: str = "json"


class ParseResponseError(AppExceptionError):
    """Exception raised for errors in parsing HTTP responses."""

    default_message: str = "Failed to parse response from external service."


# Mapping HTTP status codes to custom exceptions
HTTP_STATUS_EXCEPTION_MAPPING = {
    400: HttpResponseError(message="Bad Request", status_code=400),
    401: HttpResponseError(message="Unauthorized", status_code=401),
    403: HttpResponseError(message="Forbidden", status_code=403),
    404: HttpResponseError(message="Not Found", status_code=404),
    405: HttpMethodeNotAllowedError(),
    408: HTTPConnectionError(message="Request Timeout", status_code=408),
    500: HttpResponseError(message="Internal Server Error", status_code=500),
    502: HttpResponseError(message="Bad Gateway", status_code=502),
    503: HTTPConnectionError(message="Service Unavailable", status_code=503),
    504: HTTPConnectionError(message="Gateway Timeout", status_code=504),
}


def get_exception_for_status(
    status_code: int,
    cause: Exception | None = None,
    message: str | None = None,
    context: dict | None = None,
) -> AppExceptionError:
    """Get exception instance from mapping based on HTTP status code."""
    exc = HTTP_STATUS_EXCEPTION_MAPPING.get(status_code)
    if exc:
        # Create a new instance to avoid sharing state
        new_exc = exc.__class__(
            message=message or exc.message,
            status_code=exc.status_code,
            context=context or exc.context,
            cause=cause,
        )
        return new_exc
    # Fallback to generic response error
    return HttpResponseError(
        message=message or f"Error with status code {status_code}",
        status_code=status_code,
        context=context,
        cause=cause,
    )


class AuthenticationError(AppExceptionError):
    """Exception raised for authentication errors."""

    default_message: str = "Authentication failed."
    status_code: int = 401
    return_type: str = "json"


class AuthMemberInactiveError(AuthenticationError):
    """Exception raised for inactive member authentication errors."""

    default_message: str = "Member is inactive."
    status_code: int = 403
    return_type: str = "json"


class AuthMemberIPNotAllowedError(AuthenticationError):
    """Exception raised for IP address not allowed errors."""

    default_message: str = "IP address not allowed."
    status_code: int = 403
    return_type: str = "json"


class AuthInvalidSignatureError(AuthenticationError):
    """Exception raised for invalid signature errors."""

    default_message: str = "Invalid signature."
    status_code: int = 403
    return_type: str = "json"
