from sqlalchemy import select

from app.db.connector import async_session_maker
from app.models import UserModel
from app.services.auth import get_password_hash


async def create_user(*, username: str, password: str, email: str) -> UserModel:
    user = UserModel(username=username, password=get_password_hash(password), email=email)

    async with async_session_maker() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def find_users(username: str = "", email: str = "") -> list[UserModel]:
    query = select(UserModel).order_by(UserModel.created_at.desc())

    if username:
        query = query.where(UserModel.username == username)

    if email:
        query = query.where(UserModel.email.ilike(f"%{email}%"))

    async with async_session_maker() as session:
        result = await session.execute(query)

    return list(result.scalars())
