from fastapi import APIRouter, Depends, Header
from core.fastapi.dependencies import get_repository
from typing import Annotated
from api.block.dto import BlockResponseDTO
from core.db.repository import DatabaseRepository
from app.models.block import Block
from uuid import UUID, uuid4


workspace_router = APIRouter(prefix="/workspace", tags=["workspace"])


BlockRepository = Annotated[
    DatabaseRepository[Block],
    Depends(get_repository(Block)),
]


@workspace_router.get(
    "/",
    response_model=BlockResponseDTO,
    responses={
        200: {"description": "Block data retrieved successfully."},
        404: {"description": "Block not found."},
    },
)
async def get_workspace_route(
    x_user_id: Annotated[UUID, Header()], block_repo: BlockRepository
):
    """
    Get workspace block by user_id in X-User-Id header. The operation returns workspace block data that associated with provided user_id. Or creates and returns workspace data if it has not yet been created.
    """

    workspace = await block_repo.get(
        Block.user_id == x_user_id, Block.type == "workspace"
    )

    if workspace:

        return BlockResponseDTO.model_validate(workspace)

    id = uuid4()

    new_block = {
        "id": id,
        "type": "workspace",
        "properties": {},
        "content": [],
        "parent": id,
        "user_id": x_user_id,
    }

    block = await block_repo.create(**new_block)

    return block
