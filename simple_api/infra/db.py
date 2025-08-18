from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from simple_api.core.config import settings

_engine: AsyncEngine | None = None
_SessionLocal: async_sessionmaker | None = None


def init_engine() -> None:
    global _engine, _SessionLocal
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    _engine = create_async_engine(
        settings.database_url,
        echo=settings.env != "prod",
        pool_size=10,
        max_overflow=20,
    )
    _SessionLocal = async_sessionmaker(bind=_engine, expire_on_commit=False)


def get_engine() -> AsyncEngine:
    if _engine is None:
        init_engine()
    return _engine


def get_sessionmaker() -> async_sessionmaker:
    if _SessionLocal is None:
        init_engine()
    return _SessionLocal


class Base(DeclarativeBase):
    metadata = MetaData(schema="public")


@asynccontextmanager
async def get_db():
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session
