"""setup middleware."""

import time

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware untuk log semua request + response time."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # log incoming request
        logger.bind(
            path=request.url.path,
            method=request.method,
            client=request.client.host if request.client else "unknown",
            query_params=dict(request.query_params),
            # headers=dict(request.headers),
        ).info("Incoming request")

        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # log outgoing response
        logger.bind(
            status_code=response.status_code,
            path=request.url.path,
            process_time=process_time,
        ).info("Response sent")

        # optionally, bisa tambah header X-Process-Time
        response.headers["X-Process-Time"] = str(process_time)
        return response
