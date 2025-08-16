import uuid
from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from simple_api.infra.db import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)
    address_number = Column(String(50), nullable=False)
    address_neighborhood = Column(String(255), nullable=False)
    address_city = Column(String(255), nullable=False)
    address_state = Column(String(50), nullable=False)
    country = Column(String(3), nullable=False)
    rooms = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Numeric(10, 2), nullable=False)
