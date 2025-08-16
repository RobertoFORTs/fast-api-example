from fastapi import FastAPI, Request
from core.config import settings
from core.logging import log
from core.lifespan import lifespan
from api.v1.routers import router as v1_router

async def logging_middleware(request: Request, call_next):
    resp = await call_next(request)
    log.info(
        "request",
        method=request.method,
        path=request.url.path,
        status_code=resp.status_code,
    )
    return resp

docs_off = settings.env == "prod"
app = FastAPI(
    title=settings.app_name,
    docs_url=None if docs_off else "/docs",
    redoc_url=None if docs_off else "/redoc",
    openapi_url=None if docs_off else "/openapi.json",
    lifespan=lifespan,
)

app.middleware("http")(logging_middleware)
app.include_router(v1_router, prefix="/api/v1")
