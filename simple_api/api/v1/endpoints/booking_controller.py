from typing import List, Optional
from fastapi import APIRouter, Depends
from simple_api.schemas.booking import BookingCreate, BookingResponse, BookingResponseWithPrice
from simple_api.domain.booking.booking_service import BookingService
from simple_api.dependencies.booking_deps import get_booking_service

router = APIRouter()

@router.post("/", response_model=BookingResponseWithPrice)
async def create_booking(
    booking_in: BookingCreate,
    service: BookingService = Depends(get_booking_service),
):
    return await service.create_booking(booking_in)

@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    property_id: Optional[str] = None, 
    client_email: Optional[str] = None,
    service: BookingService = Depends(get_booking_service),
    ):
    return await service.list_bookings(property_id=property_id, client_email=client_email)