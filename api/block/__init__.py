from typing import Annotated
from fastapi import APIRouter, Header, status, Depends, HTTPException, status
from uuid import UUID
from app.services.block import BlockService, get_block_service
from core.fastapi.dependencies import get_repository
from app.models.block import Block
from core.db.repository import DatabaseRepository

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
async def get_block_route(
    id: UUID,
    x_user_id: Annotated[UUID, Header()],
    block_service: Annotated[BlockService, Depends(get_block_service())],
):
    """
    Get block. The operation returns block data that associated with provided id.
    """

    try:
        data = await block_service.get(x_user_id, id)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {
                "error_message": f"Error occurred while retrieving block.",
                "error_code": 1,
            },
        )

    if data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Block not found.", "error_code": 2},
        )

    return BlockResponseDTO(
        id=data.id,
        type=data.type,
        properties=data.properties,
        content=data.content,
        parent=data.parent,
    )


@block_router.post(
    "/",
    response_model=BlockResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Block created successfully."},
    },
)
async def create_block_route(
    data: BlockCreateRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_service: Annotated[BlockService, Depends(get_block_service())],
):
    """
    Create block. The operation creates new block with provided data.
    """

    try:
        data = await block_service.create(x_user_id, data.model_dump())
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"error_message": str(e), "error_code": 3},
        )

    return BlockResponseDTO(
        id=data.id,
        type=data.type,
        properties=data.properties,
        content=data.content,
        parent=data.parent,
    )


@block_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Block deleted successfully."},
    },
)
async def delete_block_route(
    id: UUID,
    x_user_id: Annotated[UUID, Header()],
    block_service: Annotated[BlockService, Depends(get_block_service())],
):
    """
    Delete block. The operation deletes block that associated with provided id.
    """
    try:
        await block_service.delete(x_user_id, id)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"error_message": f"Error occurred while deleting block.", "error_code": 1},
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
async def update_block_route(
    id: UUID,
    data: BlockPutRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_service: Annotated[BlockService, Depends(get_block_service())],
):
    """
    Update block. The operation updates block with provided data.
    """

    data = await block_service.update(x_user_id, id, data.model_dump())

    return BlockResponseDTO(
        id=data.id,
        type=data.type,
        properties=data.properties,
        content=data.content,
        parent=data.parent,
    )


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
async def partially_update_block_route(
    id: UUID,
    data: BlockPatchRequestDTO,
    x_user_id: Annotated[UUID, Header()],
    block_service: Annotated[BlockService, Depends(get_block_service())],
):
    """
    Partially update block. The operation partially updates block with provided data.
    """

    data = await block_service.update(
        x_user_id, id, {k: v for k, v in data.model_dump().items() if v is not None}
    )

    return BlockResponseDTO(
        id=data.id,
        type=data.type,
        properties=data.properties,
        content=data.content,
        parent=data.parent,
    )
