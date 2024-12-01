from uuid import UUID
from pydantic import BaseModel


class WorkspaceBase(BaseModel):
    owner_id: UUID
    content: list[str]


class WorkspaceResponseDTO(WorkspaceBase):
    id: UUID
