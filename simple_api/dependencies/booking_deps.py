from fastapi import Depends
from simple_api.dependencies.property_deps import get_property_repository
from simple_api.infra.repositories.booking_repository import BookingRepository
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.domain.booking.booking_service import BookingService


def get_booking_repository() -> BookingRepository:
    return BookingRepository()

def get_booking_service(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    property_repo: PropertyRepository = Depends(get_property_repository),
) -> BookingService:
    return BookingService(booking_repo, property_repo)
