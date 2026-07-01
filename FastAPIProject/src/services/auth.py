import secrets
from datetime import datetime
from typing import Annotated

import bcrypt
import binascii

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException, Depends, WebSocket
from fastapi.security import OAuth2PasswordBearer

from src.db.connector import get_session, async_session_maker
from src.dto.auth import UserDTO, ApiTokenDTO
from src.models import APITokenModel, UserModel

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_key(length: int = 20) -> str:
    return binascii.hexlify(secrets.token_bytes(length)).decode("utf-8")


async def create_user_api_token(session: AsyncSession, username: str, password: str) -> ApiTokenDTO:
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user: UserModel | None = result.scalar_one_or_none()

    if user is None or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    api_token = APITokenModel(user_id=user.id, key=generate_key(64))
    session.add(api_token)
    await session.commit()
    await session.refresh(api_token)
    return ApiTokenDTO(id=api_token.id, user_id=api_token.user_id, key=api_token.key)


async def get_token_user(session, token: str) -> UserDTO | None:
    result = await session.execute(
        select(UserModel)
        .join(APITokenModel, APITokenModel.user_id == UserModel.id)
        .where(APITokenModel.key == token)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    await session.execute(
        update(APITokenModel).where(APITokenModel.key == token).values(last_used=datetime.now())
    )

    return UserDTO.from_model(user)


async def current_user(
    token: Annotated[str, Depends(oauth_schema)],
    session: Annotated[AsyncSession, Depends(get_session, use_cache=True)],
) -> UserDTO:
    user: UserDTO | None = await get_token_user(session, token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return user


async def get_user_and_ws(ws: WebSocket) -> tuple[UserDTO, WebSocket] | None:
    auth_header = ws.headers.get("authorization")
    if auth_header is None:
        await ws.close()
        return None

    parts = auth_header.split()
    if len(parts) != 2:
        await ws.close()
        return None

    if parts[0].lower() != "bearer":
        await ws.close()
        return None

    token = parts[1]

    async with async_session_maker() as session:
        user: UserDTO | None = await get_token_user(session, token)

    if user is None:
        await ws.close()
        return None

    return user, ws
