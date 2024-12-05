from uuid import uuid4
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.block import Block
from core.db.session import get_db_session
from core.fastapi.dependencies import get_repository
from . import WorkspaceService


@pytest.fixture
async def _session() -> AsyncSession:
    """Fixture that provides a database session for testing."""
    async for session in get_db_session():
        yield session


@pytest.fixture
async def repo(_session):
    return get_repository(Block)(_session)


@pytest.fixture
async def ws(repo):
    return WorkspaceService(repo)


@pytest.fixture
def _uuid():
    return uuid4()


_uuid1 = _uuid
_uuid2 = _uuid


async def test_get(_uuid, ws):
    data = await ws.get(_uuid)

    assert data.user_id == _uuid
    assert data.type == "workspace"
    assert data.properties == {}
    assert data.content == []
    assert data.parent == data.id


async def test_get_created(_uuid, ws):
    data1 = await ws.get(_uuid)

    data2 = await ws.get(_uuid)

    assert data1.id == data2.id
    assert data1.user_id == data2.user_id
    assert data1.type == data2.type
    assert data1.properties == data2.properties
    assert data1.content == data2.content
    assert data1.parent == data2.parent
