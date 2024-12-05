import uuid
from pydantic import BaseModel
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


class BlockSchema(BaseModel):
    id: uuid.UUID
    type: str
    properties: dict
    content: list[uuid.UUID]
    parent: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True
