from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ClientContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.client_type = request.headers.get("X-Client-Type", "web")
        return await call_next(request)
