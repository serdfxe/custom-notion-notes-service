from uuid import UUID, uuid4

from fastapi import Depends
from app.models.block import Block
from app.services import Service
from core.db.repository import DatabaseRepository
from core.fastapi.dependencies import get_repository


class WorkspaceService(Service):
    async def _create(self, user_id: UUID) -> Block:
        id = uuid4()

        return await self.repo.create(
            id=id,
            user_id=str(user_id),
            type="workspace",
            properties=dict(),
            content=[],
            parent=id,
        )

    async def get(self, user_id: UUID) -> Block:
        ws = await self.repo.get(Block.user_id == user_id, Block.type == "workspace")

        if ws is None:
            ws = await self._create(user_id)

        return ws


def get_workspace_service():
    def func(repo: DatabaseRepository[Block] = Depends(get_repository(Block))):
        return WorkspaceService(repo)

    return func
