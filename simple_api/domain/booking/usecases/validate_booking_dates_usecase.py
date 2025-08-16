from datetime import date

class ValidateBookingDatesUseCase:
    def execute(self, start_date: date, end_date: date) -> None:
        """Garante que a data final é maior que a inicial."""
        raise NotImplementedError
