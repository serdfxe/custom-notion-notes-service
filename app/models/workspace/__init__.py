from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

from uuid import UUID, uuid4


class Workspace(DeclarativeBase):
    __tablename__ = 'workspaces'

    id = Column(UUID, ForeignKey("blocks.id"), primary_key=True, default=uuid4)
    owner_id = Column(UUID, primary_key=True)
    block = relationship("Block")
    