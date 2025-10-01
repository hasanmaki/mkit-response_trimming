"""base client initialization."""

import httpx
from httpx_retries import Retry, RetryTransport


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        retries: int = 3,
        backoff_factor: float = 1.0,
        headers: dict[str, str] | None = None,
    ):
        retry = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist={500, 502, 503, 504, 429},
        )
        transport = RetryTransport(retry=retry)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            transport=transport,
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def close(self):
        await self._client.aclose()
