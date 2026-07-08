from src.domain.users import User

from ..auth import get_password_hash
from .repo import AbstractUserRepository


class UserApplicationHandler:

    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def handle_register(self, username: str, password: str) -> User:
        password_hash = get_password_hash(password)

        user = User.create(username=username, password=password_hash)

        return await self.repo.add(user)
