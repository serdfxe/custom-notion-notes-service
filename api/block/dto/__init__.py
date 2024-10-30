from uuid import UUID
from pydantic import BaseModel


class BlockBase(BaseModel):
    type: str
    properties: dict
    content: list[str]
    parent: UUID
    
    class Config:
        from_attributes = True

class BlockCreateRequestDTO(BlockBase):
    ...
    
class BlockPutRequestDTO(BlockBase):
    ...
    
class BlockResponseDTO(BlockBase):
    id: UUID
