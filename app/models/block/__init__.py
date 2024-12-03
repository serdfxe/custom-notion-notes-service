from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class Block(Base):
    __tablename__ = "blocks"

    type = Column(String, nullable=False)
    properties = Column(JSON, nullable=False)
    content = Column(JSON, nullable=False)
    parent = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
