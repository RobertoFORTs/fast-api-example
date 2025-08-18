import pytest
import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from simple_api.domain.property.property_service import PropertyService
from simple_api.schemas.property import (
    PropertyCreate,
    PropertyResponse,
    PropertyFilter,
    PaginatedPropertyResponse
)

@pytest.fixture
def property_repo():
    return AsyncMock()

@pytest.fixture
def property_service(property_repo):
    return PropertyService(property_repo)

@pytest.fixture
def sample_property_create():
    return PropertyCreate(
        title="Casa na Praia",
        address_street="Rua das Palmeiras",
        address_number="41",
        address_neighborhood="Jurerê Internacional",
        address_city="Florianópolis",
        address_state="sc",
        country="br",
        rooms=3,
        capacity=6,
        price_per_night=Decimal("350.00")
    )

@pytest.fixture
def sample_property_model(sample_property_create):
    obj = MagicMock(**sample_property_create.model_dump())
    obj.id = uuid.uuid4()
    return obj



@pytest.mark.asyncio
async def test_create_property_success(property_service, property_repo, sample_property_create, sample_property_model):
    property_repo.create.return_value = sample_property_model

    result: PropertyResponse = await property_service.create_property(sample_property_create)

    property_repo.create.assert_awaited_once()
    assert result.id == sample_property_model.id
    assert result.title == sample_property_create.title
    assert result.address_state == "SC"
    assert result.country == "BR"



@pytest.mark.asyncio
async def test_list_properties_success(property_service, property_repo, sample_property_model):
    filters = PropertyFilter(address_city="Florianópolis")

    property_repo.get_filtered.return_value = {
        "total": 2,
        "items": [sample_property_model, sample_property_model]
    }

    result: PaginatedPropertyResponse = await property_service.list_properties(filters)

    property_repo.get_filtered.assert_awaited_once_with(filters)
    assert result.total == 2
    assert len(result.items) == 2
    assert all(isinstance(p, PropertyResponse) for p in result.items)
    for p in result.items:
        assert p.address_state == "SC"
        assert p.country == "BR"
