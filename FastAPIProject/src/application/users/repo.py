from abc import ABC, abstractmethod

from src.domain.users import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id_: int) -> User:
        """Если не найден, то вернет ошибку ObjectNotFound"""

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_filtered(self, page: int, page_size: int, username: str = "") -> tuple[list[User], int]: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, id_: int) -> User: ...
