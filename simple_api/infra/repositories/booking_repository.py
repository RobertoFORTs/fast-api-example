from simple_api.infra.models.booking import Booking
from simple_api.infra.repositories.base_repository import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self):
        super().__init__(Booking)