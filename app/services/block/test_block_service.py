from uuid import uuid4
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.block import Block
from app.services.workspace import WorkspaceService
from core.db.session import get_db_session
from core.fastapi.dependencies import get_repository
from . import BlockService


@pytest.fixture
async def _session() -> AsyncSession:
    """Fixture that provides a database session for testing."""
    async for session in get_db_session():
        yield session


@pytest.fixture
async def repo(_session):
    return get_repository(Block)(_session)


@pytest.fixture
async def bs(repo):
    return BlockService(repo)


@pytest.fixture
def _uuid():
    return uuid4()


_uuid1 = _uuid
_uuid2 = _uuid


@pytest.fixture
async def ws(repo):
    return WorkspaceService(repo)


@pytest.fixture
async def block(_uuid1, _uuid2, ws):
    data = await ws.get(_uuid2)

    return {
        "id": _uuid1,
        "type": "test",
        "properties": dict(),
        "content": [],
        "parent": data.id,
        "user_id": _uuid2,
    }


async def test_get(block, bs, repo):
    await repo.create(**block)
    data = await bs.get(block["user_id"], block["id"])

    assert data

    assert data.id == block["id"]
    assert data.type == block["type"]
    assert data.properties == block["properties"]
    assert data.content == block["content"]
    assert data.parent == block["parent"]
    assert data.user_id == block["user_id"]


async def test_create(block, bs):
    data = await bs.create(block["user_id"], block)

    assert data

    assert data.type == block["type"]
    assert data.properties == block["properties"]
    assert data.content == block["content"]
    assert data.parent == block["parent"]
    assert data.user_id == block["user_id"]

    data = await bs.get(data.user_id, data.id)

    assert data

    assert data.type == block["type"]
    assert data.properties == block["properties"]
    assert data.content == block["content"]
    assert data.parent == block["parent"]
    assert data.user_id == block["user_id"]


async def test_update(block, bs, repo):
    await repo.create(**block)

    data = await bs.update(block["user_id"], block["id"], {"type": "updated"})

    assert data

    assert data.id == block["id"]
    assert data.type == "updated"
    assert data.properties == block["properties"]
    assert data.content == block["content"]
    assert data.parent == block["parent"]
    assert data.user_id == block["user_id"]

    data = await bs.get(data.user_id, data.id)

    assert data

    assert data.id == block["id"]
    assert data.type == "updated"
    assert data.properties == block["properties"]
    assert data.content == block["content"]
    assert data.parent == block["parent"]
    assert data.user_id == block["user_id"]


async def test_delete(block, bs, repo):
    await repo.create(**block)

    await bs.delete(block["user_id"], block["id"])

    data = await bs.get(block["user_id"], block["id"])

    assert not data
