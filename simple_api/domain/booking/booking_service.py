from simple_api.infra.models.booking import Booking
from simple_api.infra.repositories.booking_repository import BookingRepository
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.schemas.booking import BookingCreate, BookingResponse
from simple_api.domain.booking.usecases.check_availability_usecase import CheckAvailabilityUseCase
from simple_api.domain.booking.usecases.validate_booking_dates_usecase import ValidateBookingDatesUseCase
from simple_api.domain.booking.usecases.calculate_booking_price_usecase import CalculateBookingPriceUseCase


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        property_repo: PropertyRepository,
        check_availability_uc: CheckAvailabilityUseCase,
        validate_dates_uc: ValidateBookingDatesUseCase,
        calc_price_uc: CalculateBookingPriceUseCase
    ):
        self.booking_repo = booking_repo
        self.property_repo = property_repo
        self.check_availability_uc = check_availability_uc
        self.validate_dates_uc = validate_dates_uc
        self.calc_price_uc = calc_price_uc

    async def create_booking(self, booking_in: BookingCreate) -> BookingResponse:
  
        property_obj = await self.property_repo.get_by_id(booking_in.property_id)
        if not property_obj:
            raise ValueError("Property Not Found")

        self.validate_dates_uc.execute(booking_in.start_date, booking_in.end_date)

        await self.check_availability_uc.execute(
            booking_in.property_id, booking_in.start_date, booking_in.end_date
        )
        
        exceeds_maximum_capacity = booking_in.guests_quantity > property_obj.capacity

        if exceeds_maximum_capacity:
            raise ValueError("Number of guests exceeds maximum capacity")

        price = self.calc_price_uc.execute(
            property_obj.price_per_night, booking_in.start_date, booking_in.end_date
        )

        booking_obj = Booking(**booking_in.model_dump())
        created = await self.booking_repo.create(booking_obj)

        return BookingResponse.model_validate({
            **created.__dict__,
            "price": price
        })
