from fastapi import Depends
from simple_api.infra.repositories.property_repository import PropertyRepository
from simple_api.domain.property.property_service import PropertyService

def get_property_repository() -> PropertyRepository:
    return PropertyRepository()

def get_property_service(
    repository: PropertyRepository = Depends(get_property_repository),
) -> PropertyService:
    return PropertyService(repository)
