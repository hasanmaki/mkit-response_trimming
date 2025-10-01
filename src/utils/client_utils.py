"""factory to build httpx client with retries, timeout, and wait."""

import httpx
from httpx_retries import Retry, RetryTransport
from loguru import logger


def build_async_client(
    base_url: str,
    timeout: int = 10,
    retries: int = 3,
    backoff_factor: float = 1.0,
    headers: dict[str, str] | None = None,
) -> httpx.AsyncClient:
    """Membangun httpx.AsyncClient dengan retry, timeout, dan wait."""
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist={500, 502, 503, 504, 429},
    )
    transport = RetryTransport(retry=retry)
    headers = {}
    client = httpx.AsyncClient(
        base_url=base_url,
        timeout=timeout,
        transport=transport,
        headers=headers,
    )
    return client


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
