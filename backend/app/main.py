import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.domain.exceptions import DomainError
from app.infrastructure.db.client import close_db, init_db
from app.presentation.api.v1.router import api_router
from app.presentation.container import container
from app.presentation.limiter import limiter
from app.presentation.middleware.client_context import ClientContextMiddleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    await container.categories.seed_defaults()
    yield
    await close_db()


app = FastAPI(title="MicroAvito", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ClientContextMiddleware)


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError):
    codes = {
        "not_found": 404,
        "forbidden": 403,
        "unauthorized": 401,
        "insufficient_funds": 402,
        "conflict": 409,
        "validation_error": 422,
    }
    return JSONResponse(
        status_code=codes.get(exc.code, 400),
        content={"code": exc.code, "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request: Request, exc: RequestValidationError):
    messages: list[str] = []
    for err in exc.errors():
        msg = err.get("msg", "Ошибка валидации")
        if msg.startswith("Value error, "):
            msg = msg.removeprefix("Value error, ")
        messages.append(msg)
    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": "; ".join(messages) if messages else "Ошибка валидации",
        },
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.state.limiter = limiter
app.include_router(api_router, prefix="/api")

os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
