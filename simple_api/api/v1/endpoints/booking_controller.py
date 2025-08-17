from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from datetime import date
from simple_api.schemas.booking import BookingCreate, BookingFilter, BookingResponseWithPrice, PaginatedBookingResponse
from simple_api.domain.booking.booking_service import BookingService
from simple_api.dependencies.booking_deps import get_booking_service

class BookingController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        self.router.post("/", response_model=BookingResponseWithPrice)(self.create_booking)
        self.router.get("/", response_model=PaginatedBookingResponse)(self.list_bookings)
        self.router.delete("/{booking_id}")(self.cancel_booking)
        self.router.get("/properties/{property_id}/availability")(self.check_availability)

    async def create_booking(self, booking_in: BookingCreate, service: BookingService = Depends(get_booking_service)):
        return await service.create_booking(booking_in)

    async def list_bookings(self, filters: BookingFilter = Depends(), service: BookingService = Depends(get_booking_service)):
        return await service.list_bookings(filters)

    async def cancel_booking(self, booking_id: UUID, service: BookingService = Depends(get_booking_service)):
        await service.cancel_booking(booking_id)
        return {"message": "Reserva cancelada com sucesso"}

    async def check_availability(self, property_id: UUID, start_date: date, end_date: date, service: BookingService = Depends(get_booking_service)):
        available = await service.is_available(property_id, start_date, end_date)
        return {"available": available}


