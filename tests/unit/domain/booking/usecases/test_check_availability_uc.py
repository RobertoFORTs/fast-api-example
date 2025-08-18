from datetime import date
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from simple_api.domain.booking.usecases.check_availability_usecase import CheckAvailabilityUseCase


@pytest.mark.asyncio
async def test_check_availability_success():
    repository = AsyncMock()
    repository.get_overlapping_bookings.return_value = []
    usecase = CheckAvailabilityUseCase(repository)

    result = await usecase.execute(uuid4(), date(2026, 1, 1), date(2026, 1, 5))
    assert result is True
    repository.get_overlapping_bookings.assert_awaited_once()

@pytest.mark.asyncio
async def test_check_availability_not_available():
    repository = AsyncMock()
    repository.get_overlapping_bookings.return_value = [1]
    usecase = CheckAvailabilityUseCase(repository)

    result = await usecase.execute(uuid4(), date(2026, 1, 1), date(2026, 1, 5))
    assert result is False
    repository.get_overlapping_bookings.assert_awaited_once()