from typing import Annotated
from fastapi import APIRouter, Header
from uuid import UUID

from .dto import (
    BlockPatchRequestDTO,
    BlockResponseDTO,
    BlockCreateRequestDTO,
    BlockPutRequestDTO,
)


block_router = APIRouter(prefix="/block", tags=["block"])


@block_router.get(
    "/{id}",
    response_model=BlockResponseDTO,
    responses={
        200: {"description": "Block data retrieved successfully."},
        404: {"description": "Block not found."},
    },
)
async def get_block_route(id: UUID, x_user_id: Annotated[str, Header()]):
    """
    Get block. The operation returns block data that associated with provided id.
    """


@block_router.post(
    "/",
    response_model=BlockResponseDTO,
    responses={
        200: {"description": "Block created successfully."},
        404: {"description": "Parent block not found."},
    },
)
async def create_block_route(
    request: BlockCreateRequestDTO, x_user_id: Annotated[str, Header()]
):
    """
    Create block. The operation creates new block with provided data.
    """


@block_router.delete(
    "/{id}",
    responses={
        200: {"description": "Block deleted successfully."},
        404: {"description": "Block not found."},
    },
)
async def delete_block_route(id: UUID, x_user_id: Annotated[str, Header()]):
    """
    Delete block. The operation deletes block that associated with provided id.
    """


@block_router.put(
    "/{id}",
    responses={
        200: {"description": "Block data updated successfully."},
        404: {"description": "Block not found."},
    },
)
async def update_block_route(
    id: UUID, request: BlockPutRequestDTO, x_user_id: Annotated[str, Header()]
):
    """
    Update block. The operation updates block with provided data.
    """


@block_router.patch(
    "/{id}",
    responses={
        200: {"description": "Block data partially updated successfully."},
        404: {"description": "Block not found."},
    },
)
async def update_block_route(
    id: UUID, request: BlockPatchRequestDTO, x_user_id: Annotated[str, Header()]
):
    """
    Partially update block. The operation partially updates block with provided data.
    """
