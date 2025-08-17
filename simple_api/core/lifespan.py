from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from infra.db import engine
from core.logging import log
from scripts.init_db import init_properties, init_bookings

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application startup")
    try:
        async with engine.connect() as conn:
            log.info("Database connection successful!")

        properties = await init_properties()
        await init_bookings(properties)
        log.info("Database initialized with mock data!")

    except SQLAlchemyError as e:
        log.error("Database connection failed!", error=str(e))
        raise
    except Exception as e:
        log.error("DB initialization failed!", error=str(e))
        raise

    yield  

    log.info("Application shutdown")
