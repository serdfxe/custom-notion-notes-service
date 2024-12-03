from uuid import UUID
from pydantic import BaseModel


class WorkspaceBase(BaseModel):
    owner_id: UUID
    content: list[UUID]


class WorkspaceResponseDTO(WorkspaceBase):
    id: UUID
