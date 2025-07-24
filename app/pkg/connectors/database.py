"""Connection to database."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

from app.pkg.settings import settings

__all__ = ("Base", "get_async_db", "engine")


Base = declarative_base()

engine = create_engine(
    settings.DATABASE.get_dsn(),
)

async_engine = create_async_engine(
    settings.DATABASE.get_dsn(is_async=True),
    pool_recycle=1800
)

_async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
)


async def get_async_db() -> AsyncSession:
    async with _async_session() as session:
        yield session
