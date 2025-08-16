from sqlalchemy import func
from sqlalchemy.future import select
from simple_api.infra.models.property import Property
from simple_api.infra.repositories.base_repository import BaseRepository
from simple_api.schemas.property import PaginatedPropertyResponse, PropertyFilter

class PropertyRepository(BaseRepository[Property]):
    def __init__(self):
        super().__init__(Property)

    async def get_filtered(self, filters: PaginatedPropertyResponse):
        async for db in self._get_session():
            base_query = select(self.model)

            if filters.address_neighborhood:
                base_query = base_query.where(self.model.address_neighborhood.ilike(f"%{filters.address_neighborhood}%"))
            if filters.address_city:
                base_query = base_query.where(self.model.address_city.ilike(f"%{filters.address_city}%"))
            if filters.address_state:
                base_query = base_query.where(self.model.address_state.ilike(f"%{filters.address_state}%"))
            if filters.capacity:
                base_query = base_query.where(self.model.capacity >= filters.capacity)
            if filters.max_price:
                base_query = base_query.where(self.model.price_per_night <= filters.max_price)

            offset = (filters.skip - 1) * filters.limit
            paginated_query = base_query.offset(offset).limit(filters.limit)
            result = await db.execute(paginated_query)
            items = result.scalars().all()

            count_query = select(func.count()).select_from(base_query.subquery())
            total_result = await db.execute(count_query)
            total = total_result.scalar_one()

            return {"items": items, "total": total}