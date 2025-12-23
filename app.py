from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from password_checker import PasswordChecker
import os
import time
import logging
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from password_checker import PasswordChecker


LOG = logging.getLogger("password_api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple per-IP sliding-window rate limiter.

    Not perfect for horizontal scaling (in-memory), but simple and dependency-free.
    """

    def __init__(self, app, calls: int = 30, window: int = 60):
        super().__init__(app)
        self.calls = calls
        self.window = window
        self.storage = {}  # ip -> list[timestamps]

    async def dispatch(self, request: Request, call_next: Callable):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        timestamps = self.storage.get(client, [])
        # prune
        timestamps = [t for t in timestamps if now - t < self.window]
        import sys
        import os
        import time
        import logging
        from typing import Callable

        # If running under Python 3.13+, FastAPI / Pydantic compatibility may fail.
        # Check Python version early and provide a clear error to avoid obscure import-time
        # tracebacks. If you really want to run under 3.13, set ENV var
        # "ALLOW_PYTHON_3_13" to "1" (not recommended for production).
        if sys.version_info >= (3, 13) and os.getenv("ALLOW_PYTHON_3_13") != "1":
            raise RuntimeError(
                "This project requires Python 3.11 for FastAPI/Pydantic compatibility. "
                "Create a Python 3.11 venv or use the included Dockerfile. See README.md for instructions."
            )

        from fastapi import FastAPI, HTTPException, Request, status
        from pydantic import BaseModel
        from starlette.middleware.base import BaseHTTPMiddleware
        from password_checker import PasswordChecker


        LOG = logging.getLogger("password_api")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


        class RateLimitMiddleware(BaseHTTPMiddleware):
            """Simple per-IP sliding-window rate limiter.

            Not perfect for horizontal scaling (in-memory), but simple and dependency-free.
            """

            def __init__(self, app, calls: int = 30, window: int = 60):
                super().__init__(app)
                self.calls = calls
                self.window = window
                self.storage = {}  # ip -> list[timestamps]

            async def dispatch(self, request: Request, call_next: Callable):
                client = request.client.host if request.client else "unknown"
                now = time.time()
                timestamps = self.storage.get(client, [])
                # prune
                timestamps = [t for t in timestamps if now - t < self.window]
                if len(timestamps) >= self.calls:
                    LOG.warning("Rate limit exceeded for %s", client)
                    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")
                timestamps.append(now)
                self.storage[client] = timestamps
                response = await call_next(request)
                return response


        class ContentLengthLimitMiddleware(BaseHTTPMiddleware):
            def __init__(self, app, max_size: int = 4096):
                super().__init__(app)
                self.max_size = max_size

            async def dispatch(self, request: Request, call_next: Callable):
                # Check Content-Length header quickly
                cl = request.headers.get("content-length")
                if cl is not None:
                    try:
                        if int(cl) > self.max_size:
                            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Payload too large")
                    except ValueError:
                        pass
                return await call_next(request)


        app = FastAPI(title="Password Strength API")
        app.add_middleware(RateLimitMiddleware, calls=int(os.getenv("RATE_LIMIT_CALLS", "30")), window=int(os.getenv("RATE_LIMIT_WINDOW", "60")))
        app.add_middleware(ContentLengthLimitMiddleware, max_size=int(os.getenv("MAX_REQUEST_SIZE", "4096")))

        checker = PasswordChecker()


        class PasswordRequest(BaseModel):
            password: str


        def _require_api_key(request: Request) -> None:
            api_key = os.getenv("PASSWORD_API_KEY")
            if not api_key:
                return None
            header = request.headers.get("x-api-key")
            if header != api_key:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")


        @app.post("/check")
        async def check(request: Request, payload: PasswordRequest):
            _require_api_key(request)
            if not payload.password:
                raise HTTPException(status_code=400, detail="password must be provided")
            LOG.info("Password check request from %s", request.client.host if request.client else "unknown")
            result = checker.check_password_strength(payload.password)
            return result


        @app.get("/health")
        def health():
            return {"status": "ok"}
