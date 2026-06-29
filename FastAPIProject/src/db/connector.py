from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker as create_async_session_maker

from src.settings import settings

async_engine = create_async_engine(settings.database_url)
async_session_maker = create_async_session_maker(bind=async_engine, autocommit=False, autoflush=False)


async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
