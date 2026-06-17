from sqlalchemy import select

from ..db.connector import async_session_maker
from ..models import UserModel


async def get_user_by_id(id_: int) -> UserModel:
    query = select(UserModel).where(UserModel.id == id_)
    async with async_session_maker() as session:
        result = await session.execute(query)  # (UserModel, )

    return result.scalar()  # UserModel


async def create_user(*, tg_id: int, username: str) -> UserModel:
    user = UserModel(id=tg_id, username=username)

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def find_users(username: str = "") -> list[UserModel]:
    query = select(UserModel).order_by(UserModel.created_at.desc())

    if username:
        query = query.where(UserModel.username == username)

    async with async_session_maker() as session:
        result = await session.execute(query)

    return list(result.scalars())
