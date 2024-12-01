from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class Block(Base):
    __tablename__ = "blocks"

    type = Column(String, nullable=False)
    properties = Column(JSON, nullable=False)
    content = Column(String, nullable=False)
    parent = Column(UUID(as_uuid=True), nullable=False)
