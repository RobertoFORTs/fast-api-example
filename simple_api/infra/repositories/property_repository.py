from simple_api.infra.models.property import Property
from simple_api.infra.repositories.base_repository import BaseRepository

class PropertyRepository(BaseRepository[Property]):
    def __init__(self):
        super().__init__(Property)