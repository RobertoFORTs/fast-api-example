from datetime import date
from decimal import Decimal
from simple_api.infra.models.property import Property

class CalculateBookingPriceUseCase:
    def execute(self, property: Property, start_date: date, end_date: date) -> Decimal:
        """Calcula o preço total da reserva com base nas diárias."""
        raise NotImplementedError
