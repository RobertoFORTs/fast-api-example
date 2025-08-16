from datetime import date
from uuid import UUID
from simple_api.infra.repositories.booking_repository import BookingRepository


class CheckAvailabilityUseCase:
    def __init__(self, repository: BookingRepository):
        self.repository = repository

    async def execute(self, property_id: UUID, start_date: date, end_date: date) -> None:
        """Verifica se existe sobreposição de reservas para o imóvel."""
        raise NotImplementedError
