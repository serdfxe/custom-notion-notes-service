import asyncio
from fastapi import APIRouter
from uuid import UUID, uuid4

from api.workspace import PAGES, WS

from .dto import BlockResponseDTO, BlockCreateRequestDTO, BlockPutRequestDTO


block_router = APIRouter(prefix="/block", tags=["block"])


block_db = {
    "537905d5-09c9-48ae-8012-436475ae1df8": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 1"]]
        },
        content=[
            "525134ce-19f0-4535-b052-039ea3644935",
            "41ecb4fd-59e7-4e51-83ec-638a60af0be4",
        ],
        parent=PAGES[7],
        id="537905d5-09c9-48ae-8012-436475ae1df8",
    ),
    "525134ce-19f0-4535-b052-039ea3644935": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 2"]]
        },
        content=[
            "9e4a904f-6ea2-4e0d-9dc0-190cba3799f3",
            "6f7282d9-de13-4ea2-a799-c454b65f52fb",
        ],
        parent="537905d5-09c9-48ae-8012-436475ae1df8",
        id="525134ce-19f0-4535-b052-039ea3644935",
    ),
    "41ecb4fd-59e7-4e51-83ec-638a60af0be4": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 3"]]
        },
        content=[
            "ac657a1b-3602-4b4e-a2fb-c12c38a1c0b7",
            "cd579f9d-5321-4e97-8fa4-26aaa9062028",
        ],
        parent="537905d5-09c9-48ae-8012-436475ae1df8",
        id="41ecb4fd-59e7-4e51-83ec-638a60af0be4",
    ),
    "6f7282d9-de13-4ea2-a799-c454b65f52fb": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 4"]]
        },
        content=[],
        parent=uuid4(),
        id=uuid4(),
    ),
    "9e4a904f-6ea2-4e0d-9dc0-190cba3799f3": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 5"]]
        },
        content=[
            "e2460223-997b-4914-8806-a8841fd0026d",
        ],
        parent="525134ce-19f0-4535-b052-039ea3644935",
        id="9e4a904f-6ea2-4e0d-9dc0-190cba3799f3",
    ),

    "e2460223-997b-4914-8806-a8841fd0026d": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 6"]]
        },
        content=[],
        parent="9e4a904f-6ea2-4e0d-9dc0-190cba3799f3",
        id="e2460223-997b-4914-8806-a8841fd0026d",
    ),
    "ac657a1b-3602-4b4e-a2fb-c12c38a1c0b7": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 7"]]
        },
        content=[],
        parent="41ecb4fd-59e7-4e51-83ec-638a60af0be4",
        id="ac657a1b-3602-4b4e-a2fb-c12c38a1c0b7",
    ),
    "cd579f9d-5321-4e97-8fa4-26aaa9062028": BlockResponseDTO(
        type="text",
        properties={
            "text": [["Text Content. 8"]]
        },
        content=[],
        parent="41ecb4fd-59e7-4e51-83ec-638a60af0be4",
        id="cd579f9d-5321-4e97-8fa4-26aaa9062028",
    ),
    # WORKSPACE
    WS: BlockResponseDTO(
        type="workspace",
        properties={},
        content=[
            PAGES[0], PAGES[1], PAGES[2], 
        ],
        parent=WS,
        id=WS,
    ),
    # PAGES
    PAGES[0]: BlockResponseDTO(
        type="folder",
        properties={
            "title": [["Folder 1"]]
        },
        content=[PAGES[3], PAGES[4]],
        parent=WS,
        id=PAGES[0],
    ),
    PAGES[1]: BlockResponseDTO(
        type="folder",
        properties={
            "title": [["Folder 2"]]
        },
        content=[PAGES[5], PAGES[6]],
        parent=WS,
        id=PAGES[1],
    ),
    PAGES[2]: BlockResponseDTO(
        type="folder",
        properties={
            "title": [["Folder 3"]],
        },
        content=[],
        parent=WS,
        id=PAGES[2],
    ),
    PAGES[3]: BlockResponseDTO(
        type="folder",
        properties={
            "title": [["Folder 4"]],
            "emoji": [['📄']],
        },
        content=[PAGES[7]],
        parent=PAGES[0],
        id=PAGES[3],
    ),
    PAGES[4]: BlockResponseDTO(
        type="page",
        properties={
            "title": [['Page 2.']],
            "emoji": [['📄']],
        },
        content=[],
        parent=PAGES[0],
        id=PAGES[4],
    ),
    PAGES[5]: BlockResponseDTO(
        type="page",
        properties={
            "title": [['Page 3.']],
            "emoji": [['📄']],
        },
        content=[],
        parent=PAGES[0],
        id=PAGES[5],
    ),
    PAGES[6]: BlockResponseDTO(
        type="page",
        properties={
            "title": [['Page 4.']],
            "emoji": [['📄']],
        },
        content=[],
        parent=PAGES[0],
        id=PAGES[6],
    ),
    PAGES[7]: BlockResponseDTO(
        type="page",
        properties={
            "title": [['Page 1.']],
            "emoji": [['🦍']],# [['📄']],
        },
        content=[
            "537905d5-09c9-48ae-8012-436475ae1df8",
        ],
        parent=PAGES[0],
        id=PAGES[7],
    ),
}

"""
[0]
    [3]
        [7]
    [4]
[1]
    [5]
    [6]
[2]
"""

@block_router.get('/{id}', response_model=BlockResponseDTO, responses={
    200: {"description": "Block data retrieved successfully."},
    404: {"description": "Block not found."},
})
async def get_block_route(id: UUID):
    """
    Get block. The operation returns block data that associated with provided id. 
    """

    return block_db[str(id)]

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
async def delete_block_route(id: UUID):
    """
    Delete block. The operation deletes block that associated with provided id. 
    """

@block_router.put("/{id}", responses={
    200: {"description": "Block data updated successfully."},
    404: {"description": "Block not found."},
})
async def update_block_route(id: UUID, request: BlockPutRequestDTO):
    """
    Update block. The operation updates block with provided data.
    """

    block_db[str(id)] = BlockResponseDTO(id=id, **dict(request))
