from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date
from decimal import Decimal


class BookingCreate(BaseModel):
    property_id: UUID = Field(
        ...,
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    client_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        pattern=r'^[a-zA-Z\s]+$',
        example="John Doe"
    )
    client_email: EmailStr = Field(
        ...,
        example="john.doe@example.com"
    )
    start_date: date = Field(
        ...,
        example="2026-01-01"
    )
    end_date: date = Field(
        ...,
        example="2026-01-05"
    )
    guests_quantity: int = Field(
        ...,
        gt=0,
        example=2
    )

class BookingFilter(BaseModel):
    property_id: Optional[UUID] = None
    client_email: Optional[EmailStr] = None
    skip: int = Field(1, ge=1)
    limit: int = Field(50, ge=1, le=500)

class BookingResponseWithPrice(BookingCreate):
    id: UUID
    price: Decimal

    model_config = {
        "from_attributes": True
    }

class BookingResponse(BookingCreate):
    id: UUID

    model_config = {
        "from_attributes": True
    }

class PaginatedBookingResponse(BaseModel):
    total: int
    items: List[BookingResponse]
