from fastapi import APIRouter
from pydantic import UUID1

from dto import WorkspaceResponseDTO


workspace_router = APIRouter(prefix="workspace", tags=["block"])

@workspace_router.get('/', response_model=WorkspaceResponseDTO, responses={
    200: {"description": "Block data retrieved successfully."},
    404: {"description": "Block not found."},
})
async def get_workspace_route():
    """
    Get workspace block by user_id in X-User-Id header. The operation returns workspace block data that associated with provided user_id. Or creates and returns workspace data if it has not yet been created.
    """
