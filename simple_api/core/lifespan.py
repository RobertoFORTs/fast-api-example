# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from simple_api.core.logging import log

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup")
    yield
    log.info("shutdown")
