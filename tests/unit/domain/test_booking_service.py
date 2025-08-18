import pytest
import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from simple_api.core.config import Settings
from simple_api.domain.booking.booking_service import BookingService
from simple_api.schemas.booking import BookingCreate, BookingResponseWithPrice
from simple_api.domain.exceptions.domain_exception import NotFoundException, ConflictException, ValidationException

@pytest.fixture(autouse=True)
def fake_settings(monkeypatch):
    monkeypatch.setattr(
        "simple_api.core.config.settings",
        Settings(database_url="sqlite:///:memory:", app_name="test", env="test")
    )


@pytest.mark.asyncio
async def test_create_booking_success():
    # --- Arrange ---
    fake_property_id = uuid.uuid4()

    booking_in = BookingCreate(
        property_id=fake_property_id,
        client_name="Maria Pereira",
        client_email="mariapereira@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 5),
        guests_quantity=4,
    )

    # Mock property
    property_obj = MagicMock()
    property_obj.capacity = 6
    property_obj.price_per_night = 100

    # Mocks dos repos/usecases
    booking_repo = AsyncMock()
    booking_repo.create.return_value = MagicMock(**booking_in.model_dump(), id=uuid.uuid4())

    property_repo = AsyncMock()
    property_repo.get_by_id.return_value = property_obj

    check_availability_uc = AsyncMock()
    check_availability_uc.execute.return_value = True

    validate_dates_uc = MagicMock()
    calc_price_uc = MagicMock()
    calc_price_uc.execute.return_value = 400  # 4 nights * 100

    service = BookingService(
        booking_repo,
        property_repo,
        check_availability_uc,
        validate_dates_uc,
        calc_price_uc,
    )

    # --- Act ---
    result: BookingResponseWithPrice = await service.create_booking(booking_in)

    # --- Assert ---
    property_repo.get_by_id.assert_called_once_with(fake_property_id)
    validate_dates_uc.execute.assert_called_once()
    check_availability_uc.execute.assert_called_once()
    booking_repo.create.assert_called_once()
    calc_price_uc.execute.assert_called_once()

    assert result.price == 400
    assert result.client_name == "Maria Pereira"


@pytest.mark.asyncio
async def test_create_booking_property_not_found():
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=2,
    )

    booking_repo = AsyncMock()
    property_repo = AsyncMock()
    property_repo.get_by_id.return_value = None

    service = BookingService(
        booking_repo, property_repo, AsyncMock(), MagicMock(), MagicMock()
    )

    with pytest.raises(NotFoundException):
        await service.create_booking(booking_in)


@pytest.mark.asyncio
async def test_create_booking_not_available():
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=2,
    )

    property_obj = MagicMock()
    property_obj.capacity = 4
    property_obj.price_per_night = 100

    booking_repo = AsyncMock()
    property_repo = AsyncMock()
    property_repo.get_by_id.return_value = property_obj

    check_availability_uc = AsyncMock()
    check_availability_uc.execute.return_value = False

    service = BookingService(
        booking_repo, property_repo, check_availability_uc, MagicMock(), MagicMock()
    )

    with pytest.raises(ConflictException):
        await service.create_booking(booking_in)


@pytest.mark.asyncio
async def test_create_booking_exceeds_capacity():
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=10,  # maior que a capacidade
    )

    property_obj = MagicMock()
    property_obj.capacity = 5
    property_obj.price_per_night = 100

    booking_repo = AsyncMock()
    property_repo = AsyncMock()
    property_repo.get_by_id.return_value = property_obj

    service = BookingService(
        booking_repo, property_repo, AsyncMock(return_value=True), MagicMock(), MagicMock()
    )

    with pytest.raises(ValidationException):
        await service.create_booking(booking_in)
