from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends

from src.domain.users import User
from src.application.auth import get_user_and_ws
from src.application.chat import handle_websocket

router = APIRouter(prefix="", tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(
    user_and_ws: Annotated[tuple[User, WebSocket] | None, Depends(get_user_and_ws)],
):
    if user_and_ws is None:
        return

    user, ws = user_and_ws

    await ws.accept()
    await handle_websocket(user, ws)
