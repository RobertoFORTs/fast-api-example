from pydantic import BaseModel
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
