from datetime import date, timedelta

import pytest
from simple_api.domain.booking.usecases.validate_booking_dates_usecase import ValidateBookingDatesUseCase
from simple_api.domain.exceptions.domain_exception import ValidationException


def test_validate_booking_dates_success():
    usecase = ValidateBookingDatesUseCase()
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=3)

    usecase.execute(start, end)

def test_validate_booking_dates_in_past():
    usecase = ValidateBookingDatesUseCase()
    start = date.today() - timedelta(days=1)
    end = date.today() + timedelta(days=1)

    with pytest.raises(ValidationException) as exc:
        usecase.execute(start, end)
    assert "passadas" in str(exc.value)

def test_validate_booking_dates_end_before_start():
    usecase = ValidateBookingDatesUseCase()
    start = date.today() + timedelta(days=5)
    end = date.today() + timedelta(days=3)

    with pytest.raises(ValidationException) as exc:
        usecase.execute(start, end)
    assert "posterior" in str(exc.value)