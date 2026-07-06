from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.users.handlers import UserApplicationHandler
from src.application.api_tokens.handlers import ApiTokenApplicationHandler
from src.application.users.repo import AbstractUserRepository
from src.application.api_tokens.repo import AbstractAPITokenRepository
from src.infrastructure.db.connector import get_session
from src.infrastructure.db.repos.users import SQLUserRepository
from src.infrastructure.db.repos.api_tokens import SQLAPITokenRepository


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session, use_cache=True)],
) -> AbstractUserRepository:
    return SQLUserRepository(session)


def get_users_app_handler(
    repo: Annotated[AbstractUserRepository, Depends(get_user_repository, use_cache=True)],
) -> UserApplicationHandler:
    return UserApplicationHandler(repo=repo)


def get_api_token_repository(
    session: Annotated[AsyncSession, Depends(get_session, use_cache=True)],
) -> AbstractAPITokenRepository:
    return SQLAPITokenRepository(session)


def get_api_tokens_app_handler(
    repo: Annotated[AbstractAPITokenRepository, Depends(get_user_repository, use_cache=True)],
) -> ApiTokenApplicationHandler:
    return ApiTokenApplicationHandler(repo=repo)
