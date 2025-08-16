from typing import List
from fastapi import APIRouter, Depends, Query
from simple_api.schemas.property import PaginatedPropertyResponse, PropertyCreate, PropertyFilter, PropertyResponse
from simple_api.dependencies.property_deps import get_property_service
from simple_api.domain.property.property_service import PropertyService

router = APIRouter()

@router.post("/", response_model= PropertyResponse)
async def create_property(
    property_in: PropertyCreate,
    service: PropertyService = Depends(get_property_service),
):
    return await service.create_property(property_in)

@router.get("/", response_model= PaginatedPropertyResponse)
async def list_properties(
    filters: PropertyFilter = Depends(),
    service: PropertyService = Depends(get_property_service),
):
    return await service.list_properties(filters)