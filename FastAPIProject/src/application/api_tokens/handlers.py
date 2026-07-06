from src.domain.api_tokens import ApiToken
from .repo import AbstractAPITokenRepository
from ..auth import verify_password
from ..users.repo import AbstractUserRepository
from ...domain.exceptions import ObjectNotFound
from ...domain.users import User


class ApiTokenApplicationHandler:

    def __init__(self, token_repo: AbstractAPITokenRepository, users_repo: AbstractUserRepository):
        self.token_repo = token_repo
        self.users_repo = users_repo

    async def handle_create_api_token(self, username: str, password: str) -> ApiToken:
        user: User | None = await self.users_repo.get_by_username(username)
        if user is None or not verify_password(password, user.password):
            raise ObjectNotFound("Неверное имя пользователя или пароль")

        api_key = ApiToken.create(user_id=user.id)

        return await self.token_repo.add(api_key)
