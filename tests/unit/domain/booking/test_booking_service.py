import pytest
import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from simple_api.domain.booking.booking_service import BookingService
from simple_api.schemas.booking import (
    BookingCreate, BookingFilter, BookingResponseWithPrice, 
    BookingResponse, PaginatedBookingResponse
)
from simple_api.domain.exceptions.domain_exception import (
    NotFoundException, ConflictException, ValidationException
)

@pytest.fixture
def booking_repo():
    return AsyncMock()

@pytest.fixture
def property_repo():
    return AsyncMock()

@pytest.fixture
def check_availability_uc():
    return AsyncMock()

@pytest.fixture
def validate_dates_uc():
    return MagicMock()

@pytest.fixture
def calc_price_uc():
    return MagicMock()

@pytest.fixture
def booking_service(booking_repo, property_repo, check_availability_uc, validate_dates_uc, calc_price_uc):
    return BookingService(
        booking_repo,
        property_repo,
        check_availability_uc,
        validate_dates_uc,
        calc_price_uc
    )

@pytest.mark.asyncio
async def test_create_booking_success(booking_service, booking_repo, property_repo, check_availability_uc, validate_dates_uc, calc_price_uc):
    fake_property_id = uuid.uuid4()
    booking_in = BookingCreate(
        property_id=fake_property_id,
        client_name="Maria Pereira",
        client_email="mariapereira@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 5),
        guests_quantity=4,
    )

    property_obj = MagicMock(capacity=6, price_per_night=100)
    property_repo.get_by_id.return_value = property_obj

    booking_repo.create.return_value = MagicMock(**booking_in.model_dump(), id=uuid.uuid4())
    check_availability_uc.execute.return_value = True
    calc_price_uc.execute.return_value = 400

    result: BookingResponseWithPrice = await booking_service.create_booking(booking_in)

    property_repo.get_by_id.assert_called_once_with(fake_property_id)
    validate_dates_uc.execute.assert_called_once()
    check_availability_uc.execute.assert_called_once()
    booking_repo.create.assert_called_once()
    calc_price_uc.execute.assert_called_once()

    assert result.price == 400
    assert result.client_name == "Maria Pereira"


@pytest.mark.asyncio
async def test_create_booking_property_not_found(booking_service, property_repo):
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=2,
    )

    property_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await booking_service.create_booking(booking_in)


@pytest.mark.asyncio
async def test_create_booking_not_available(booking_service, property_repo, check_availability_uc):
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=2,
    )

    property_obj = MagicMock(capacity=4, price_per_night=100)
    property_repo.get_by_id.return_value = property_obj
    check_availability_uc.execute.return_value = False

    with pytest.raises(ConflictException):
        await booking_service.create_booking(booking_in)


@pytest.mark.asyncio
async def test_create_booking_exceeds_capacity(booking_service, property_repo):
    booking_in = BookingCreate(
        property_id=uuid.uuid4(),
        client_name="John Doe",
        client_email="john@example.com",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        guests_quantity=10,
    )

    property_obj = MagicMock(capacity=5, price_per_night=100)
    property_repo.get_by_id.return_value = property_obj

    with pytest.raises(ValidationException):
        await booking_service.create_booking(booking_in)


@pytest.mark.asyncio
async def test_list_bookings_success(booking_service, booking_repo):
    filters = BookingFilter(property_id=uuid.uuid4())
    
    booking_items = [
        MagicMock(
            id=uuid.uuid4(),
            property_id=uuid.uuid4(),
            client_name="Alice",
            client_email="alice@example.com",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 5),
            guests_quantity=2
        ),
        MagicMock(
            id=uuid.uuid4(),
            property_id=uuid.uuid4(),
            client_name="Bob",
            client_email="bob@example.com",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 5),
            guests_quantity=3
        ),
    ]
    booking_repo.get_filtered.return_value = {"total": 2, "items": booking_items}

    result: PaginatedBookingResponse = await booking_service.list_bookings(filters)

    booking_repo.get_filtered.assert_called_once_with(filters)
    assert result.total == 2
    assert len(result.items) == 2
    assert all(isinstance(b, BookingResponse) for b in result.items)



@pytest.mark.asyncio
async def test_cancel_booking_success(booking_service, booking_repo):
    booking_id = uuid.uuid4()
    booking_obj = MagicMock(id=booking_id)
    booking_repo.get_by_id.return_value = booking_obj

    await booking_service.cancel_booking(booking_id)

    booking_repo.get_by_id.assert_called_once_with(booking_id)
    booking_repo.delete.assert_called_once_with(booking_id)


@pytest.mark.asyncio
async def test_cancel_booking_not_found(booking_service, booking_repo):
    booking_id = uuid.uuid4()
    booking_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await booking_service.cancel_booking(booking_id)


@pytest.mark.asyncio
async def test_is_available_success(booking_service, property_repo, check_availability_uc, validate_dates_uc):
    property_id = uuid.uuid4()
    start_date = date(2026, 1, 1)
    end_date = date(2026, 1, 5)

    property_obj = MagicMock()
    property_repo.get_by_id.return_value = property_obj
    check_availability_uc.execute.return_value = True

    result = await booking_service.is_available(property_id, start_date, end_date)

    property_repo.get_by_id.assert_called_once_with(property_id)
    validate_dates_uc.execute.assert_called_once_with(start_date, end_date)
    check_availability_uc.execute.assert_called_once_with(property_id, start_date, end_date)
    assert result is True


@pytest.mark.asyncio
async def test_is_available_property_not_found(booking_service, property_repo):
    property_id = uuid.uuid4()
    start_date = date(2026, 1, 1)
    end_date = date(2026, 1, 5)

    property_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await booking_service.is_available(property_id, start_date, end_date)
