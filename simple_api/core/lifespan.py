from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from infra.db import engine
from core.logging import log

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application startup")
    try:
        with engine.connect() as conn:
            log.info("Database connection successful!")
    except SQLAlchemyError as e:
        log.error("Database connection failed!", error=str(e))
        raise

    yield

    log.info("Application shutdown")
