from fastapi import APIRouter, Depends, Header
from app.services.workspace import WorkspaceService, get_workspace_service
from core.fastapi.dependencies import get_repository
from typing import Annotated
from api.block.dto import BlockResponseDTO
from core.db.repository import DatabaseRepository
from app.models.block import Block
from uuid import UUID, uuid4


workspace_router = APIRouter(prefix="/workspace", tags=["workspace"])


@workspace_router.get(
    "/",
    response_model=BlockResponseDTO,
    responses={
        200: {"description": "Block data retrieved successfully."},
        404: {"description": "Block not found."},
    },
)
async def get_workspace_route(
    x_user_id: Annotated[UUID, Header()],
    workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service())],
):
    """
    Get workspace block by user_id in X-User-Id header. The operation returns workspace block data that associated with provided user_id. Or creates and returns workspace data if it has not yet been created.
    """

    workspace = await workspace_service.get(x_user_id)

    return workspace
