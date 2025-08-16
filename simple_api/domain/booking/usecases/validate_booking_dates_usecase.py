from datetime import date

class ValidateBookingDatesUseCase:
    def execute(self, start_date: date, end_date: date) -> None:
        
        if start_date < date.today():
            raise ValueError("Não é possível fazer reservas em datas passadas")

        if end_date <= start_date:
            raise ValueError("A data final deve ser posterior à data inicial")
