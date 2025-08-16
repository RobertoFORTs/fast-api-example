import uuid
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from simple_api.infra.db import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    guests_quantity = Column(Integer, nullable=False)
