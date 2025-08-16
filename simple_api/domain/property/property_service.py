# domain/property/property_service.py
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.schemas.property import PropertyCreate, PropertyResponse
from simple_api.infra.models.property import Property

class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    async def create_property(self, property_in: PropertyCreate) -> PropertyResponse:
        prop_obj = Property(**property_in.model_dump())
        created = await self.repository.create(prop_obj)
        return PropertyResponse.model_validate(created)
