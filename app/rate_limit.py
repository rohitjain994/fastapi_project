import time
from typing import Dict, Tuple

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class InMemoryRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.requests = requests
        self.window_seconds = window_seconds
        self.buckets: Dict[str, Tuple[int, float]] = {}

    def _key_from_request(self, request: Request) -> str:
        client = request.client.host if request.client else "unknown"
        path = request.url.path
        return f"{client}:{path}"

    async def dispatch(self, request: Request, call_next) -> Response:
        key = self._key_from_request(request)
        now = time.time()
        count, window_start = self.buckets.get(key, (0, now))

        if now - window_start >= self.window_seconds:
            count = 0
            window_start = now

        count += 1
        self.buckets[key] = (count, window_start)

        if count > self.requests:
            retry_after = int(self.window_seconds - (now - window_start))
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
                headers={"Retry-After": str(max(retry_after, 1))},
            )

        response = await call_next(request)
        remaining = max(self.requests - count, 0)
        response.headers["X-RateLimit-Limit"] = str(self.requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(window_start + self.window_seconds))
        return response


