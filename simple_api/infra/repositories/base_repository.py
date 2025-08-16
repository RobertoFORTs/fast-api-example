from typing import Type, TypeVar, Generic, AsyncGenerator
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from simple_api.infra.db import get_db

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def _get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager para obter sessão automaticamente"""
        async with get_db() as session:
            yield session

    async def get_all(self):
        async for db in self._get_session():
            result = await db.execute(select(self.model))
            return result.scalars().all()

    async def get_by_id(self, id):
        async for db in self._get_session():
            result = await db.execute(select(self.model).where(self.model.id == id))
            return result.scalar_one_or_none()

    async def create(self, obj_in: T):
        async for db in self._get_session():
            db.add(obj_in)
            await db.commit()
            await db.refresh(obj_in)
            return obj_in

    async def delete(self, id):
        async for db in self._get_session():
            stmt = delete(self.model).where(self.model.id == id)
            result = await db.execute(stmt)
            await db.commit()
            return result.rowcount
