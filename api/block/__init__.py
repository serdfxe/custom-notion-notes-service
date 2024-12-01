from typing import Annotated
from fastapi import APIRouter, Header, status
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
        status.HTTP_200_OK: {"description": "Block data retrieved successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
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
        status.HTTP_201_CREATED: {"description": "Block created successfully."},
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
        status.HTTP_204_NO_CONTENT: {"description": "Block deleted successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def delete_block_route(id: UUID, x_user_id: Annotated[str, Header()]):
    """
    Delete block. The operation deletes block that associated with provided id.
    """


@block_router.put(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"description": "Block data updated successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
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
        status.HTTP_200_OK: {"description": "Block data partially updated successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def update_block_route(
    id: UUID, request: BlockPatchRequestDTO, x_user_id: Annotated[str, Header()]
):
    """
    Partially update block. The operation partially updates block with provided data.
    """
