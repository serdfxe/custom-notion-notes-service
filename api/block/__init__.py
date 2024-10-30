from fastapi import APIRouter
from pydantic import UUID1

from .dto import BlockResponseDTO, BlockCreateRequestDTO, BlockPutRequestDTO


block_router = APIRouter(prefix="/block", tags=["block"])

@block_router.get('/{id}', response_model=BlockResponseDTO, responses={
    200: {"description": "Block data retrieved successfully."},
    404: {"description": "Block not found."},
})
async def get_block_route(id: UUID1):
    """
    Get block. The operation returns block data that associated with provided id. 
    """

@block_router.post("/", response_model=BlockResponseDTO, responses={
    200: {"description": "Block created successfully."},
    404: {"description": "Parent block not found."},
})
async def create_block_route(request: BlockCreateRequestDTO):
    """
    Create block. The operation creates new block with provided data.
    """

@block_router.delete("/{id}", responses={
    200: {"description": "Block deleted successfully."},
    404: {"description": "Block not found."},
})
async def delete_block_route(id: UUID1):
    """
    Delete block. The operation deletes block that associated with provided id. 
    """

@block_router.put("/{id}", responses={
    200: {"description": "Block data updated successfully."},
    404: {"description": "Block not found."},
})
async def update_block_route(id: UUID1, request: BlockPutRequestDTO):
    """
    Update block. The operation updates block with provided data.
    """
