from sqlalchemy import BigInteger, Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin


class Block(Base, TimestampMixin):
    __tablename__ = 'blocks'

    type = Column(String, nullable=False)
    content = Column(String, nullable=False)
