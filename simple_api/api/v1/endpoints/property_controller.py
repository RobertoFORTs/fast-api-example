from fastapi import APIRouter, Depends
from simple_api.schemas.property import PropertyCreate, PropertyResponse
from simple_api.dependencies.property_deps import get_property_service
from simple_api.domain.property.property_service import PropertyService

router = APIRouter()

@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_in: PropertyCreate,
    service: PropertyService = Depends(get_property_service),
):
    return await service.create_property(property_in)
