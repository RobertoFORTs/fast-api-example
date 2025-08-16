from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

class PropertyCreate(BaseModel):
    title: str
    address_street: str
    address_number: str
    address_neighborhood: str
    address_city: str
    address_state: str
    country: str
    rooms: int
    capacity: int
    price_per_night: Decimal

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
