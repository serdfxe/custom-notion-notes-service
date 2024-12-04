from typing import Annotated
from fastapi import APIRouter, Header, status, Depends, HTTPException, status
from uuid import UUID
from core.fastapi.dependencies import get_repository
from app.models.block import Block
from core.db.repository import DatabaseRepository

from .dto import (
    BlockPatchRequestDTO,
    BlockResponseDTO,
    BlockCreateRequestDTO,
    BlockPutRequestDTO,
)

BlockRepository = Annotated[
    DatabaseRepository[Block],
    Depends(get_repository(Block)),
]

block_router = APIRouter(prefix="/block", tags=["block"])


@block_router.get(
    "/{id}",
    response_model=BlockResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Block data retrieved successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def get_block_route(
    id: UUID, x_user_id: Annotated[UUID, Header()], block_repo: BlockRepository
):
    """
    Get block. The operation returns block data that associated with provided id.
    """

    data = await block_repo.get(Block.id == id, Block.user_id == x_user_id)

    if data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found.", "error_code": 1},
        )

    return data


@block_router.post(
    "/",
    response_model=BlockResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Block created successfully."},
    },
)
async def create_block_route(
    request: BlockCreateRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_repo: BlockRepository,
):
    """
    Create block. The operation creates new block with provided data.
    """

    new_block_data = {
        "type": request.type,
        "properties": request.properties,
        "content": request.content,
        "parent": request.parent,
        "user_id": x_user_id,
    }
    new_block = await block_repo.create(**new_block_data)

    return new_block


@block_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Block deleted successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def delete_block_route(
    id: UUID, x_user_id: Annotated[UUID, Header()], block_repo: BlockRepository
):
    """
    Delete block. The operation deletes block that associated with provided id.
    """

    data = await block_repo.get(Block.id == id, Block.user_id == x_user_id)

    if data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found.", "error_code": 2},
        )

    await block_repo.delete(Block.id == id, Block.user_id == x_user_id)

    try:
        parent = await block_repo.get(Block.id == data.parent, Block.user_id == x_user_id)

        await block_repo.update(parent.id, {
            "content": [
                child for child in parent.content
                if child["id"] != id
            ]
        })
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"error_message": f"Error occurred while updating parent block.", "error_code": 3},
        )

    return {
        "status": status.HTTP_204_NO_CONTENT,
        "detail": "Block deleted successfully",
    }


@block_router.put(
    "/{id}",
    response_model=BlockResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Block data updated successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def update_block(
    id: UUID,
    request: BlockPutRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_repo: BlockRepository,
):
    """
    Update block. The operation updates block with provided data.
    """

    data = await block_repo.get(Block.id == id, Block.user_id == x_user_id)

    if data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found.", "error_code": 3},
        )

    data = {
        "type": request.type,
        "properties": request.properties,
        "content": request.content,
        "parent": request.parent,
    }

    data = {key: val for key, val in data.items() if val is not None}

    return await block_repo.update(id, data)


@block_router.patch(
    "/{id}",
    response_model=BlockResponseDTO,
    responses={
        status.HTTP_200_OK: {
            "description": "Block data partially updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def update_block_route(
    id: UUID,
    request: BlockPatchRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_repo: BlockRepository,
):
    """
    Partially update block. The operation partially updates block with provided data.
    """

    block = await block_repo.get(Block.id == id, Block.user_id == x_user_id)

    if block is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found", "error_code": 4},
        )

    update_data = {
        "type": request.type,
        "properties": request.properties,
        "content": request.content,
        "parent": request.parent,
    }

    update_data = {
        key: value for key, value in update_data.items() if value is not None
    }

    return await block_repo.update(id, update_data)
