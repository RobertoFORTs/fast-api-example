from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from infra.db import engine  # async engine
from core.logging import log

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application startup")
    try:
        async with engine.connect() as conn:
            log.info("Database connection successful!")
    except SQLAlchemyError as e:
        log.error("Database connection failed!", error=str(e))
        raise

    yield

    log.info("Application shutdown")
