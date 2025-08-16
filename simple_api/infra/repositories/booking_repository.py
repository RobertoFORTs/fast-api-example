from datetime import date
from typing import List

from sqlalchemy import func, select
from simple_api.infra.models.booking import Booking
from simple_api.infra.repositories.base_repository import BaseRepository
from simple_api.schemas.booking import BookingFilter

class BookingRepository(BaseRepository[Booking]):
    def __init__(self):
        super().__init__(Booking)
    
    async def get_overlapping_bookings(
        self, property_id, start_date: date, end_date: date
    ) -> List[Booking]:
        """
        Retorna todas as reservas de um imóvel que colidem com o período solicitado.
        """
        async for db in self._get_session():
            query = select(self.model).where(
                (self.model.property_id == property_id) &
                (self.model.end_date > start_date) &
                (self.model.start_date < end_date) 
            )
            result = await db.execute(query)
            return result.scalars().all()
    


    async def get_filtered(self, filters: BookingFilter):
        async for db in self._get_session():
            base_query = select(self.model)

            if filters.property_id:
                base_query = base_query.where(Booking.property_id == filters.property_id)
            if filters.client_email:
                base_query = base_query.where(Booking.client_email == filters.client_email)

            offset = (filters.skip - 1) * filters.limit
            paginated_query = base_query.offset(offset).limit(filters.limit)
            result = await db.execute(paginated_query)
            items = result.scalars().all()

            count_query = select(func.count()).select_from(base_query.subquery())
            total_result = await db.execute(count_query)
            total = total_result.scalar_one()

            return {"items": items, "total": total}