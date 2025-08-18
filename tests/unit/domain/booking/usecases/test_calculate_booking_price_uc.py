from datetime import date
from decimal import Decimal

import pytest
from simple_api.domain.booking.usecases.calculate_booking_price_usecase import CalculateBookingPriceUseCase
from simple_api.domain.exceptions.domain_exception import ValidationException


def test_calculate_booking_price_success():
    usecase = CalculateBookingPriceUseCase()
    price_per_night = Decimal("100.00")
    start = date(2026, 1, 1)
    end = date(2026, 1, 5)

    result = usecase.execute(price_per_night, start, end)
    assert result == Decimal("400.00")

def test_calculate_booking_price_invalid_period():
    usecase = CalculateBookingPriceUseCase()
    price_per_night = Decimal("100.00")
    start = date(2026, 1, 5)
    end = date(2026, 1, 1) 
    
    with pytest.raises(ValidationException) as exc:
        usecase.execute(price_per_night, start, end)
    assert "inválido" in str(exc.value)
