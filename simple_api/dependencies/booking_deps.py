from fastapi import Depends
from simple_api.infra.repositories.booking_repository import BookingRepository
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.domain.booking.booking_service import BookingService
from simple_api.domain.booking.usecases.check_availability_usecase import CheckAvailabilityUseCase
from simple_api.domain.booking.usecases.validate_booking_dates_usecase import ValidateBookingDatesUseCase
from simple_api.domain.booking.usecases.calculate_booking_price_usecase import CalculateBookingPriceUseCase

def get_booking_repository() -> BookingRepository:
    return BookingRepository()

def get_property_repository() -> PropertyRepository:
    return PropertyRepository()

def get_check_availability_uc(
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> CheckAvailabilityUseCase:
    return CheckAvailabilityUseCase(booking_repo)

def get_validate_dates_uc() -> ValidateBookingDatesUseCase:
    return ValidateBookingDatesUseCase()

def get_calc_price_uc() -> CalculateBookingPriceUseCase:
    return CalculateBookingPriceUseCase()

def get_booking_service(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    property_repo: PropertyRepository = Depends(get_property_repository),
    check_availability_uc: CheckAvailabilityUseCase = Depends(get_check_availability_uc),
    validate_dates_uc: ValidateBookingDatesUseCase = Depends(get_validate_dates_uc),
    calc_price_uc: CalculateBookingPriceUseCase = Depends(get_calc_price_uc),
) -> BookingService:
    return BookingService(
        booking_repo,
        property_repo,
        check_availability_uc,
        validate_dates_uc,
        calc_price_uc,
    )
