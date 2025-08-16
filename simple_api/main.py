from fastapi import FastAPI, Request
from simple_api.core.config import settings
from simple_api.core.logging import log
from simple_api.core.lifespan import lifespan
from simple_api.api.v1.routers import router as v1_router
from fastapi.middleware.cors import CORSMiddleware
import time

async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    log.info(
        "request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=f"{duration:.3f}s"
    )
    return response


def configure_middlewares(app: FastAPI):
    app.middleware("http")(logging_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_routes(app: FastAPI):
    app.include_router(v1_router, prefix="/api/v1")

docs_disabled = settings.env == "prod"

app = FastAPI(
    title=settings.app_name,
    description="API de exemplo usando FastAPI e Poetry",
    version="1.0.0",
    docs_url=None if docs_disabled else "/docs",
    redoc_url=None if docs_disabled else "/redoc",
    openapi_url=None if docs_disabled else "/openapi.json",
    lifespan=lifespan,
)

configure_middlewares(app)

@app.get("/", tags=["root"])
async def root():
    return {"message": "API rodando. Use /api/v1/health para testar e /docs para acessar o swagger."}


configure_routes(app)
