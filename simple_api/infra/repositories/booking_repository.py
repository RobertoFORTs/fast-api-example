from datetime import date
from typing import List

from sqlalchemy import select
from simple_api.infra.models.booking import Booking
from simple_api.infra.repositories.base_repository import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self):
        super().__init__(Booking)
    
    async def get_bookings_for_property_in_period(
        self, property_id, start_date: date, end_date: date
    ) -> List[Booking]:
        """
        Retorna todas as reservas de um imóvel que colidem com o período solicitado.
        """
        async for db in self._get_session():
            query = select(self.model).where(
                (self.model.property_id == property_id) &
                (self.model.end_date >= start_date) &
                (self.model.start_date <= end_date) 
            )
            result = await db.execute(query)
            return result.scalars().all()