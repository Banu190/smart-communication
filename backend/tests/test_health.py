import asyncio
import os
from unittest.mock import AsyncMock

import httpx
import pytest
from sqlalchemy.exc import SQLAlchemyError

# An unreachable, password-free URL; every DB request uses an override.
os.environ["DATABASE_URL"] = "postgresql+asyncpg://test@127.0.0.1:1/test"
os.environ["APP_NAME"] = "SÖYLE API"
os.environ["DEBUG"] = "false"

from app.database import get_db
from app.main import app


@pytest.fixture
def db():
    session = AsyncMock()

    async def override():
        yield session

    app.dependency_overrides[get_db] = override
    try:
        yield session
    finally:
        app.dependency_overrides.clear()


def request(path):
    async def run():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.get(path)

    return asyncio.run(run())


def test_root(db):
    response = request("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SÖYLE API"}
    db.execute.assert_not_awaited()


def test_health(db):
    response = request("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    db.execute.assert_not_awaited()


def test_database_connected(db):
    response = request("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
    db.execute.assert_awaited_once()
    assert str(db.execute.call_args.args[0]) == "SELECT 1"


@pytest.mark.parametrize("error", [SQLAlchemyError("internal details"), OSError("internal details"), TimeoutError()])
def test_database_unavailable(db, error):
    db.execute.side_effect = error
    response = request("/health/db")
    assert response.status_code == 503
    assert response.json() == {
        "status": "error", "database": "unavailable",
        "message": "Database is temporarily unavailable",
    }
