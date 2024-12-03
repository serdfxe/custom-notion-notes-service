from typing import Annotated
from fastapi import APIRouter, Header, status, Depends, HTTPException, status
from uuid import UUID, uuid4
from core.fastapi.dependencies import get_repository
from app.models.block import Block
from app.models.workspace import Workspace
from core.db.repository import DatabaseRepository

from .dto import (
    BlockPatchRequestDTO,
    BlockResponseDTO,
    BlockCreateRequestDTO,
    BlockPutRequestDTO,
)

UserRepository = Annotated[
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
    id: UUID, x_user_id: Annotated[UUID, Header()], user_repo: UserRepository
):
    """
    Get block. The operation returns block data that associated with provided id.
    """

    data = await user_repo.get(Block.id == id, Block.user_id == x_user_id)

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
    user_repo: UserRepository,
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
    new_block = await user_repo.create(**new_block_data)

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
    id: UUID, x_user_id: Annotated[UUID, Header()], user_repo: UserRepository
):
    """
    Delete block. The operation deletes block that associated with provided id.
    """

    data = await user_repo.get(Block.id == id, Block.user_id == x_user_id)

    if data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found.", "error_code": 2},
        )

    await user_repo.delete(Block.id == id, Block.user_id == x_user_id)

    return {
        "status": status.HTTP_204_NO_CONTENT,
        "detail": "Block deleted successfully",
    }


@block_router.put(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"description": "Block data updated successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Block not found."},
    },
)
async def update_block(
    id: UUID,
    request: BlockPutRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    user_repo: UserRepository,
):
    """
    Update block. The operation updates block with provided data.
    """

    data = await user_repo.get(Block.id == id, Block.user_id == x_user_id)

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

    await user_repo.update(id, data)

    return {
        "status": status.HTTP_200_OK,
        "description": "Block data updated successfully.",
    }


@block_router.patch(
    "/{id}",
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
    user_repo: UserRepository,
):
    """
    Partially update block. The operation partially updates block with provided data.
    """

    block = await user_repo.get(Block.id == id, Block.user_id == x_user_id)

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

    await user_repo.update(id, update_data)

    return {
        "status": status.HTTP_200_OK,
        "description": "Block data partially updated successfully.",
    }
