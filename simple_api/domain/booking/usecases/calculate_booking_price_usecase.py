from datetime import date
from decimal import Decimal

from simple_api.domain.exceptions.domain_exception import ValidationException
from simple_api.infra.models.property import Property

class CalculateBookingPriceUseCase:
    def execute(self, price_per_night: Decimal, start_date: date, end_date: date) -> Decimal:
        num_nights = (end_date - start_date).days
        if num_nights <= 0:
            raise ValidationException("Período da reserva inválido")
        return price_per_night * num_nights
