from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from infra.db import engine, get_db
from core.logging import log
from scripts.init_db import init_properties, init_bookings
from simple_api.infra.models.db_meta import DBMeta


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application startup")
    try:
        async with engine.connect() as conn:
            log.info("Database connection successful!")

        async with get_db() as session:
            from sqlalchemy import select
            meta = await session.execute(select(DBMeta).limit(1))
            meta = meta.scalar_one_or_none()

            if not meta or not meta.initialized:
                log.info("Populating mock data...")

                properties = await init_properties()
                await init_bookings(properties)

                if not meta:
                    meta = DBMeta(initialized=True)
                    session.add(meta)
                else:
                    meta.initialized = True

                await session.commit()
                log.info("Database initialized with mock data!")
            else:
                log.info("Database already initialized, skipping mock data.")

    except SQLAlchemyError as e:
        log.error("Database connection failed!", error=str(e))
        raise
    except Exception as e:
        log.error("DB initialization failed!", error=str(e))
        raise

    yield
    log.info("Application shutdown")
