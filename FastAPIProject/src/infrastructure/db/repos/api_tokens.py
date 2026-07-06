from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.api_tokens.repo import AbstractAPITokenRepository
from src.domain.api_tokens import ApiToken
from src.infrastructure.db.exception_handler import exception_handler
from src.infrastructure.db.models import APITokenModel


class SQLAPITokenRepository(AbstractAPITokenRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_key(self, key: str) -> ApiToken:
        pass

    async def add(self, obj: ApiToken) -> ApiToken:
        token_model = APITokenModel(key=obj.key, user_id=obj.user_id, last_used=obj.last_used)

        try:
            self.session.add(token_model)
            await self.session.commit()
            await self.session.refresh(token_model)
        except SQLAlchemyError as exc:
            exception_handler(exc)

        return ApiToken(
            id=token_model.id,
            key=token_model.key,
            user_id=token_model.user_id,
            last_used=token_model.last_used,
        )

    async def delete(self, id_: int) -> ApiToken:
        pass
