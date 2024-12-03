from fastapi import APIRouter

from .dto import WorkspaceResponseDTO


USER = "cad1b2f1-e707-418f-8af2-fc7b0a4d4e26"
MAIN_CHILD = "537905d5-09c9-48ae-8012-436475ae1df8"

WS = "53106344-1f27-4651-b2ac-4837128c5adb"

PAGES = """00a498ee-e9a3-4144-b3a3-24044d012b51
525e1ce4-a9e5-4f97-9071-3ca10ab1868e
504a73c2-5f0a-4292-ad1f-42d44295fb0b
c43ee66f-1335-44d0-a1fb-a809b81aa853
5545ba9f-4dcd-4462-8d02-faae6aa57500
88dd83ac-5c62-4bd3-9143-8286fc671104
2268df32-949f-4759-a253-4cd77aa598fe
32e98562-12eb-43eb-b824-a7c82dcd89c4
af02950d-4b7a-46de-9933-7f9ebd4243ee""".split(
    "\n"
)

workspace_router = APIRouter(prefix="/workspace", tags=["workspace"])


@workspace_router.get(
    "/",
    response_model=WorkspaceResponseDTO,
    responses={
        200: {"description": "Block data retrieved successfully."},
        404: {"description": "Block not found."},
    },
)
async def get_workspace_route():
    """
    Get workspace block by user_id in X-User-Id header. The operation returns workspace block data that associated with provided user_id. Or creates and returns workspace data if it has not yet been created.
    """

    return WorkspaceResponseDTO(
        owner_id=USER, content=[PAGES[0], PAGES[1], PAGES[2]], id=WS
    )
