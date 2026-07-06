from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.users.repo import AbstractUserRepository
from src.domain.users import User
from src.infrastructure.db.exception_handler import exception_handler
from src.infrastructure.db.models import UserModel


class SQLUserRepository(AbstractUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: int) -> User | None:
        query = select(UserModel).where(UserModel.id == id_)
        result = await self.session.execute(query)  # (UserModel, )

        user_model: UserModel | None = result.scalar()
        return self._to_domain(user_model) if user_model is not None else None

    async def get_by_username(self, username: str) -> User | None:
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)  # (UserModel, )

        user_model: UserModel | None = result.scalar()
        return self._to_domain(user_model) if user_model is not None else None

    async def get_filtered(self, page: int, page_size: int, username: str = "") -> tuple[list[User], int]:
        query = select(UserModel).order_by(UserModel.created_at.desc())

        if username:
            query = query.where(UserModel.username == username)

        result = await self.session.execute(query)

        return list(result.scalars()), 0

    async def add(self, user: User) -> User:
        user_model = UserModel(username=user.username, password=user.password)

        try:
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
        except SQLAlchemyError as exc:
            exception_handler(exc)

        return self._to_domain(user_model)

    async def update(self, user: User) -> User:
        pass

    async def delete(self, id_: int) -> User:
        pass

    @staticmethod
    def _to_domain(user_model: UserModel):
        return User(
            id=user_model.id,
            username=user_model.username,
            password=user_model.password,
            created_at=user_model.created_at,
        )
