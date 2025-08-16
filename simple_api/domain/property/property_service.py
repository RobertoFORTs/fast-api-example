from typing import List, Optional
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.schemas.property import PaginatedPropertyResponse, PropertyCreate, PropertyFilter, PropertyResponse
from simple_api.infra.models.property import Property

class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    async def create_property(self, property_in: PropertyCreate) -> PropertyResponse:
        prop_obj = Property(**property_in.model_dump())
        created = await self.repository.create(prop_obj)
        return PropertyResponse.model_validate(created)

    async def list_properties(self, filters: PropertyFilter) -> PaginatedPropertyResponse:
        result = await self.repository.get_filtered(filters)

        items = [PropertyResponse.model_validate(p) for p in result["items"]]
        total = result["total"]
        
        return PaginatedPropertyResponse(total=total, items=items)