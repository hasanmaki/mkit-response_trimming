import httpx
from loguru import logger

from src.config import AppSettings
from src.custom.exceptions import HTTPConnectionError, HttpResponseError


def build_http_client(settings: AppSettings) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        headers=settings.clients.headers,
        limits=httpx.Limits(max_connections=settings.clients.max_connections),
        timeout=settings.clients.timeout,
        http2=settings.clients.http2,
    )


async def cst_get(client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response:
    """GET dengan logging + error handling standar."""
    logger.debug(f"HTTP GET {url} {kwargs}")
    try:
        response = await client.get(url, **kwargs)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"HTTP status error {exc.response.status_code} on {exc.request.url}",
            exc_info=True,
        )
        message = f"HTTP error {exc.response.status_code} from external service: {exc}"
        raise HttpResponseError(
            message=message,
            context={"url": str(exc.request.url), "response": exc.response.text},
            cause=exc,
        ) from exc
    except httpx.RequestError as exc:
        logger.error(f"HTTP connection error {exc}", exc_info=True)
        message = f"Connection error from external service: {exc}"
        raise HTTPConnectionError(
            message=message,
            context={"url": str(exc.request.url) if exc.request else url},
            cause=exc,
        ) from exc
    else:
        return response
