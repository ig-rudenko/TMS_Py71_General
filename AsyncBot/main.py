import asyncio

from app.db.connector import async_engine
from app.models import Base
from app.services.users import create_user, find_users


async def create_db_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_db_tables()

    # user = await create_user(username="admin2", password="password", email="admin2@localhost")

    users = await find_users(email="gmail")
    print(users)

if __name__ == '__main__':
    asyncio.run(main())
