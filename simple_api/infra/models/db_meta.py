import uuid
from sqlalchemy import Boolean, Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from simple_api.infra.db import Base


class DBMeta(Base):
    __tablename__ = "db_meta"
    __table_args__ = {"schema": "public"}

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    initialized = Column(Boolean, default=False, nullable=False)
