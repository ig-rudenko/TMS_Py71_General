from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket

from src.application.chat import AbstractChatManager
from src.domain.users import User

from ..auth import get_user_and_ws
from ..ws_chat_manager import get_chat_manager, handle_websocket

router = APIRouter(prefix="", tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(
    user_and_ws: Annotated[tuple[User, WebSocket] | None, Depends(get_user_and_ws)],
    chat_manager: Annotated[AbstractChatManager, Depends(get_chat_manager)],
):
    if user_and_ws is None:
        return

    user, ws = user_and_ws

    await ws.accept()
    await handle_websocket(chat_manager, user=user, ws=ws)
