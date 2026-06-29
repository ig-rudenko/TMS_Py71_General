from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import get_password_hash
from ..db.exception_handler import exception_handler
from ..models import UserModel


async def get_user_by_id(session: AsyncSession, id_: int) -> UserModel:
    query = select(UserModel).where(UserModel.id == id_)
    result = await session.execute(query)  # (UserModel, )

    return result.scalar()  # UserModel


async def create_user(session: AsyncSession, *, username: str, password: str) -> UserModel:
    user = UserModel(username=username, password=get_password_hash(password))

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except SQLAlchemyError as exc:
        exception_handler(exc)

    return user


async def find_users(session: AsyncSession, username: str = "") -> list[UserModel]:
    query = select(UserModel).order_by(UserModel.created_at.desc())

    if username:
        query = query.where(UserModel.username == username)

    result = await session.execute(query)

    return list(result.scalars())
