from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker as create_async_session_maker

from app.config import DB_URL

async_engine = create_async_engine(DB_URL)
async_session_maker = create_async_session_maker(bind=async_engine, autocommit=False, autoflush=False)
