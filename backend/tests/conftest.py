"""PostgreSQL integration harness: one disposable schema per test."""

import asyncio
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import Connection, make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

BACKEND = Path(__file__).resolve().parents[1]


def migrate(connection: Connection, revision: str, *, downgrade: bool = False) -> None:
    config = Config(str(BACKEND / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND / "alembic"))
    config.attributes["connection"] = connection
    if downgrade:
        command.downgrade(config, revision)
    else:
        command.upgrade(config, revision)


@pytest.fixture
def run_db() -> Callable[[Callable[[AsyncSession, AsyncEngine], Awaitable[None]]], None]:
    raw_url = os.environ.get("TEST_DATABASE_URL")
    if not raw_url:
        pytest.skip("Set TEST_DATABASE_URL to a dedicated PostgreSQL database ending in _test")
    url = make_url(raw_url)
    if url.drivername != "postgresql+asyncpg" or not (url.database or "").endswith("_test"):
        pytest.fail("TEST_DATABASE_URL must use postgresql+asyncpg and a database ending in _test")
    # Never fall back to DATABASE_URL or the application's .env file.
    schema = f"soyle_test_{uuid4().hex}"

    def run(case: Callable[[AsyncSession, AsyncEngine], Awaitable[None]]) -> None:
        async def execute() -> None:
            engine = create_async_engine(
                url, poolclass=NullPool,
                connect_args={"server_settings": {"search_path": schema, "timezone": "UTC"}},
            )
            try:
                async with engine.begin() as connection:
                    await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
                    await connection.run_sync(lambda sync: migrate(sync, "head"))
                async with AsyncSession(engine, expire_on_commit=False) as session:
                    await case(session, engine)
            finally:
                try:
                    async with engine.begin() as connection:
                        await connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
                finally:
                    await engine.dispose()

        asyncio.run(execute())

    return run
