import pytest

from fastapi import FastAPI

from starlette.testclient import TestClient
from uuid import UUID, uuid4

from . import block_router
from ..workspace import workspace_router


app = FastAPI()
app.include_router(block_router)
app.include_router(workspace_router)


client = TestClient(app)


@pytest.fixture
def user_id():
    return str(uuid4())


def user_headers(user_id: UUID):
    return {"X-User-Id": str(user_id)}


@pytest.fixture
def _uuid():
    return str(uuid4())


@pytest.fixture
async def ws_user(user_id):
    response = client.get(
        "/workspace/",
        headers=user_headers(user_id),
    )

    return [response.json(), user_id]


@pytest.fixture
def block(_uuid, ws_user):
    ws, user_id = ws_user

    return {
        "type": "page",
        "properties": {"title": [[f"Page {_uuid} title"]]},
        "content": [],
        "parent": str(ws["id"]),
        "user_id": user_id,
    }


async def test_create_block(user_id, block):
    response = client.post(
        "/block",
        headers=user_headers(user_id),
        json=block,
    )

    assert response.status_code == 201

    assert "id" in response.json()

    assert "type" in response.json()
    assert response.json()["type"] == block["type"]

    assert "properties" in response.json()
    assert response.json()["properties"] == block["properties"]

    assert "content" in response.json()
    assert response.json()["content"] == block["content"]

    assert "parent" in response.json()
    assert response.json()["parent"] == block["parent"]


def create_block(data: dict, user_id: UUID):
    response = client.post(
        "/block",
        headers=user_headers(user_id),
        json=data,
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def created_block_user_id(block, user_id):
    return [
        create_block(block, user_id),
        user_id,
    ]


def test_get_block(created_block_user_id: list):
    block, user_id = created_block_user_id

    response = client.get(
        f"/block/{block['id']}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 200

    assert "type" in response.json()
    assert response.json()["type"] == block["type"]

    assert "properties" in response.json()
    assert response.json()["properties"] == block["properties"]

    assert "content" in response.json()
    assert response.json()["content"] == block["content"]

    assert "parent" in response.json()
    assert response.json()["parent"] == block["parent"]

    assert "id" in response.json()
    assert response.json()["id"] == block["id"]


def test_get_block_not_found(user_id):
    response = client.get(
        f"/block/{uuid4()}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 404

    assert "detail" in response.json()

    assert "error_message" in response.json()["detail"]
    assert response.json()["detail"]["error_message"] == "Block not found."


def test_delete_block(created_block_user_id: list):
    block, user_id = created_block_user_id

    block_id = block["id"]

    response = client.delete(
        f"/block/{block_id}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 204

    response = client.get(
        f"/block/{block_id}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 404

    assert "detail" in response.json()

    assert "error_message" in response.json()["detail"]
    assert response.json()["detail"]["error_message"] == "Block not found."


def test_delete_block_not_found(user_id):
    response = client.delete(
        f"/block/{uuid4()}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 204


def test_update_block(created_block_user_id: list):
    block, user_id = created_block_user_id

    block_id = block["id"]

    new_block = {
        "type": "cool_page_type",
        "properties": {"title": [[f"Updated Page {block_id} title"]]},
        "content": [
            str(uuid4()),
        ],
        "parent": str(uuid4()),
    }

    response = client.put(
        f"/block/{block_id}",
        headers=user_headers(user_id),
        json=new_block,
    )

    assert response.status_code == 200

    response = client.get(
        f"/block/{block_id}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 200

    assert "type" in response.json()
    assert response.json()["type"] == new_block["type"]

    assert "properties" in response.json()
    assert response.json()["properties"] == new_block["properties"]

    assert "content" in response.json()
    assert response.json()["content"] == new_block["content"]

    assert "parent" in response.json()
    assert response.json()["parent"] == new_block["parent"]

    assert "id" in response.json()
    assert response.json()["id"] == block_id


@pytest.mark.parametrize(
    "new_data",
    [
        {
            "type": "type2",
        },
        {
            "properties": {"title": [[f"Updated Page title 22"]]},
        },
        {
            "content": [str(uuid4())],
        },
        {
            "parent": str(uuid4()),
        },
        {
            "type": "type2",
            "properties": {"title": [[f"Updated Page title 2"]]},
            "content": [str(uuid4())],
            "parent": str(uuid4()),
        },
    ],
)
def test_patch_block(new_data, created_block_user_id):
    block, user_id = created_block_user_id

    block_id = block["id"]

    response = client.patch(
        f"/block/{block_id}",
        headers=user_headers(user_id),
        json=new_data,
    )

    assert response.status_code == 200

    response = client.get(
        f"/block/{block_id}",
        headers=user_headers(user_id),
    )

    assert response.status_code == 200

    for prop in ["type", "id", "parent", "properties", "content"]:
        assert prop in response.json()

        if prop in new_data:
            assert response.json()[prop] == new_data[prop]
        else:
            assert response.json()[prop] == block[prop]
