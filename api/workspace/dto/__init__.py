from uuid import UUID
from api.block.dto import BlockBase


class WorkspaceBase(BlockBase):
    type: str = "workspace"
    content: list[str]
    
class WorkspaceResponseDTO(WorkspaceBase):
    owner: UUID