from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4

from core.db import Base

from app.models.block import Block


class Workspace(Base):
    __tablename__ = "workspaces"

    owner_id = Column(UUID(as_uuid=True), primary_key=True)
    block = relationship(Block, uselist=False, foreign_keys=[id])
