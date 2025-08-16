from typing import List, Optional
from fastapi import APIRouter, Depends
from datetime import date
from simple_api.schemas.booking import BookingCreate, BookingFilter, BookingResponse, BookingResponseWithPrice
from simple_api.domain.booking.booking_service import BookingService
from simple_api.dependencies.booking_deps import get_booking_service

class BookingController:
    def __init__(self, service: BookingService = Depends(get_booking_service)):
        self.service = service
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        self.router.post("/", response_model=BookingResponseWithPrice)(self.create_booking)
        self.router.get("/", response_model=List[BookingResponse])(self.list_bookings)
        self.router.delete("/{booking_id}")(self.cancel_booking)
        self.router.get("/properties/{property_id}/availability")(self.check_availability)


    async def create_booking(self, booking_in: BookingCreate):
        return await self.service.create_booking(booking_in)

    async def list_bookings(
        self,
        filters: BookingFilter = Depends(),
    ):
        return await self.service.list_bookings(filters)

    async def cancel_booking(self, booking_id: str):
        await self.service.cancel_booking(booking_id)
        return {"message": "Reserva cancelada com sucesso"}

    async def check_availability(
        self,
        property_id: str,
        start_date: date,
        end_date: date,
    ):
        available = await self.service.is_available(property_id, start_date, end_date)
        return {"available": available}

