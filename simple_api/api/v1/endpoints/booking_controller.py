from fastapi import APIRouter, Depends
from simple_api.schemas.booking import BookingCreate, BookingResponse
from simple_api.domain.booking.booking_service import BookingService
from simple_api.dependencies.booking_deps import get_booking_service

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_in: BookingCreate,
    service: BookingService = Depends(get_booking_service),
):
    return await service.create_booking(booking_in)
