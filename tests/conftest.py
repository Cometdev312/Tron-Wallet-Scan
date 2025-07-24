"""Configuration for pytest."""

import asyncio
import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.pkg.connectors.database import Base
from app.pkg.settings import settings
from app.configuration import __containers__


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case.

    Notes:
        This fixture is used for anyio tests.

    Warnings:
        Full isolation for each test case is guaranteed only if the test cases
        are executed sequentially.
    """

    _ = request
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def prepare_db():
    """Create a test database before tests and drop it after."""

    if not settings.DATABASE.DATABASE_NAME.startswith("test_"):
        settings.DATABASE.DATABASE_NAME = f"test_{settings.DATABASE.DATABASE_NAME}"

    test_database_dsn = settings.DATABASE.get_dsn(is_async=False)

    # Create test DB
    if database_exists(test_database_dsn):
        drop_database(test_database_dsn)
    create_database(test_database_dsn)

    # Create tables
    engine = create_engine(test_database_dsn)
    Base.metadata.create_all(engine)

    yield

    # Cleanup
    engine.dispose()
    drop_database(test_database_dsn)


@pytest.fixture
async def db_session(prepare_db):
    """Create a fresh DB session for each test."""

    async_engine = create_async_engine(settings.DATABASE.get_dsn(is_async=True))
    async_session = async_sessionmaker(bind=async_engine)

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
    await async_engine.dispose()


def pytest_sessionstart(session):
    _ = session

    __containers__.wire_packages(pkg_name="tests")
