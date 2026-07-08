from typing import Annotated

from fastapi import Depends, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordBearer

from src.application.api_tokens.handlers import ApiTokenApplicationHandler
from src.domain.exceptions import AuthenticationError
from src.domain.users import User

from .dependencies import get_api_tokens_app_handler

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth_schema)],
    handler: Annotated[ApiTokenApplicationHandler, Depends(get_api_tokens_app_handler)],
) -> User:
    try:
        user = await handler.get_user_by_token(token)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return user


async def get_user_and_ws(
    ws: WebSocket,
    handler: Annotated[ApiTokenApplicationHandler, Depends(get_api_tokens_app_handler)],
) -> tuple[User, WebSocket] | None:
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

    try:
        user = await handler.get_user_by_token(token)
    except AuthenticationError:
        await ws.close()
        return None

    return user, ws
