from datetime import date
from simple_api.domain.exceptions.domain_exception import ValidationException

class ValidateBookingDatesUseCase:
    def execute(self, start_date: date, end_date: date) -> None:
        
        if start_date < date.today():
            raise ValidationException("Não é possível fazer reservas em datas passadas")

        if end_date <= start_date:
            raise ValidationException("A data final deve ser posterior à data inicial")
