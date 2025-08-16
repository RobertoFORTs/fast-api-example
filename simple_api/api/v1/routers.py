from fastapi import APIRouter
from simple_api.api.v1.endpoints import health
from simple_api.api.v1.endpoints import property_controller 
from simple_api.api.v1.endpoints import booking_controller


router = APIRouter()
router.include_router(health.router, prefix="", tags=["health"])
router.include_router(property_controller.router, prefix="/properties", tags=["Properties"])
router.include_router(booking_controller.router, prefix="/bookings", tags=["Bookings"])