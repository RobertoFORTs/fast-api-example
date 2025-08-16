from datetime import date
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

@router.delete("/bookings/{booking_id}")
async def cancel_booking(
    booking_id: str,
    service: BookingService = Depends(get_booking_service),
    ):

    await service.cancel_booking(booking_id)
    return {"message": "Reserva cancelada com sucesso"}

@router.get("/properties/{property_id}/availability")
async def check_availability(property_id: str, start_date: date, end_date: date, service: BookingService = Depends(get_booking_service)):
    """
    Verificar disponibilidade de uma propriedade entre datas.
    """
    available = await service.is_available(property_id, start_date, end_date)
    return {"available": available}