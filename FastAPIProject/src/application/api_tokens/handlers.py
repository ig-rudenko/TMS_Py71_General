from src.domain.api_tokens import ApiToken

from ...domain.exceptions import AuthenticationError, ObjectNotFound
from ...domain.users import User
from ..auth import verify_password
from ..services.cache import AbstractCache
from ..users.repo import AbstractUserRepository
from .repo import AbstractAPITokenRepository


class ApiTokenApplicationHandler:

    def __init__(
        self,
        token_repo: AbstractAPITokenRepository,
        users_repo: AbstractUserRepository,
        cache: AbstractCache,
    ):
        self.token_repo = token_repo
        self.users_repo = users_repo
        self.cache = cache

    async def handle_create_api_token(self, username: str, password: str) -> ApiToken:
        user: User | None = await self.users_repo.get_by_username(username)
        if user is None or not verify_password(password, user.password):
            raise ObjectNotFound("Неверное имя пользователя или пароль")

        api_key = ApiToken.create(user_id=user.id)

        return await self.token_repo.add(api_key)

    async def get_user_by_token(self, token_key: str) -> User:
        try:
            token = await self.token_repo.get_by_key(token_key)
        except ObjectNotFound as exc:
            raise AuthenticationError("Неверный токен") from exc

        cache_key = f"user_token:{token.id}:{token.user_id}"

        cached_user: User | None = await self.cache.get(cache_key)
        if cached_user is not None:
            return cached_user

        try:
            user = await self.users_repo.get_by_id(token.user_id)
        except ObjectNotFound as exc:
            raise AuthenticationError("Пользователь не найден") from exc

        await self.cache.set(cache_key, user, timeout=60)

        return user
