import logging
import httpx
from api.block import block_router
from api.workspace import workspace_router


from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware


def init_cors(api: FastAPI) -> None:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(api: FastAPI) -> None:
    api.include_router(block_router)
    api.include_router(workspace_router)


def create_api() -> FastAPI:
    api = FastAPI(
        title="Notes Service",
        description="Hide API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    init_routers(api=api)

    return api


api = create_api()

# @api.middleware("http")
# async def verify_auth_middleware(request: Request, call_next):
#     header = request.headers.get('Authorization')
    
#     # logger = logging.getLogger(__name__)
#     # logger.setLevel(logging.ERROR)  
    
#     # logger.error(header)

#     if header is None:
#         return Response(content="Token is missing", status_code=status.HTTP_401_UNAUTHORIZED)

#     async with httpx.AsyncClient() as client:
#         verify_response = await client.get("http://localhost:8000/auth/verify", headers={
#             'Authorization': f'{header}'
#         })

#     if verify_response.status_code != status.HTTP_200_OK:
#         return Response(content="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)

#     user_id = verify_response.json().get("user_id")

#     if user_id:
#         request.headers.__dict__["_list"].append(("X-User-Id".encode(), user_id.encode()))
        
#         response = await call_next(request)
        
#         return response
#     else:
#         return Response(content="User ID not found", status_code=status.HTTP_403_FORBIDDEN)
    
init_cors(api=api)