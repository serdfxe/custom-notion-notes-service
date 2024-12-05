from uuid import UUID
from pydantic import BaseModel


class BlockBase(BaseModel):
    type: str
    properties: dict
    content: list[UUID]
    parent: UUID

    class Config:
        from_attributes = True


class BlockCreateRequestDTO(BlockBase): ...


class BlockPutRequestDTO(BlockBase): ...


class BlockPatchRequestDTO(BaseModel):
    type: str | None = None
    properties: dict | None = None
    content: list[UUID] | None = None
    parent: UUID | None = None

    class Config:
        from_attributes = True


class BlockResponseDTO(BlockBase):
    id: UUID
