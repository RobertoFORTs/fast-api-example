from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date
from decimal import Decimal


class BookingCreate(BaseModel):
    property_id: UUID
    client_name: str = Field(..., min_length=1, max_length=255)
    client_email: EmailStr
    start_date: date
    end_date: date
    guests_quantity: int = Field(..., gt=0)


class BookingResponse(BookingCreate):
    id: UUID
    price: Decimal

    model_config = {
        "from_attributes": True
    }
