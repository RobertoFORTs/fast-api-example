from datetime import date

class ValidateBookingDatesUseCase:
    def execute(self, start_date: date, end_date: date) -> None:
        if end_date <= start_date:
            raise ValueError("A data final deve ser posterior à data inicial")
