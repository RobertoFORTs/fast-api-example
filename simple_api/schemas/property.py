from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from decimal import Decimal

class PropertyCreate(BaseModel):
    title: str
    address_street: str
    address_number: str = Field(..., pattern=r"^\d+$")
    address_neighborhood: str = Field(..., pattern=r"^[a-zA-Z\s]+$")
    address_city: str = Field(..., pattern=r"^[a-zA-Z\s]+$")
    address_state: str = Field(..., min_length=2, max_length=2)
    country: str = Field(..., min_length=2, max_length=2)
    rooms: int
    capacity: int
    price_per_night: Decimal = Field(..., gt=0)

    @field_validator("address_state", "country", mode="before")
    def to_uppercase(cls, v: str) -> str:
        return v.upper() if isinstance(v, str) else v

class PropertyResponse(PropertyCreate):
    id: UUID

    model_config = {
        "from_attributes": True 
    }

class PropertyFilter(BaseModel):
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)
    max_price: Optional[float] = Field(None, gt=0)
    skip: int = Field(1, ge=1)
    limit: int = Field(100, ge=1, le=500)

class PaginatedPropertyResponse(BaseModel):
    total: int
    items: List[PropertyResponse]
