from datetime import date
from decimal import Decimal
from simple_api.infra.models.property import Property

class CalculateBookingPriceUseCase:
    def execute(self, property: Property, start_date: date, end_date: date) -> Decimal:
        num_nights = (end_date - start_date).days
        if num_nights <= 0:
            raise ValueError("Período da reserva inválido")
        return property.price_per_night * num_nights
