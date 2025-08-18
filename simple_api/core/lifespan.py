from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from simple_api.infra.db import get_db, get_engine, get_sessionmaker, init_engine
from core.logging import log
from scripts.init_db import init_properties, init_bookings
from simple_api.infra.models.db_meta import DBMeta
from simple_api.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application startup")

    try:
        init_engine()
        engine = get_engine()

        async with engine.connect() as conn:
            log.info("Database connection successful!")

        async with get_db() as session:
            from sqlalchemy import select
            meta = await session.execute(select(DBMeta).limit(1))
            meta = meta.scalar_one_or_none()

            if settings.env == "dev" and (not meta or not meta.initialized):
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
                if (settings.env=="prod"):
                    log.info("Production env, mock data skipped")
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
    await engine.dispose()
