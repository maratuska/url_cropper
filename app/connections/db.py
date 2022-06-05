from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker

from app.settings import conf


__all__ = [
    'get_session',
    'init_db_and_tables',
]


engine = create_async_engine(
    conf.db_settings.postgres_url,
    echo=True,
    future=True,
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db_and_tables():
    from app.api.models import OriginUrl, ShortUrl
    async with engine.begin() as connection:
        connection: AsyncConnection
        await connection.run_sync(SQLModel.metadata.create_all)
