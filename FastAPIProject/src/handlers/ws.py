from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends

from src.dto.auth import UserDTO
from src.services.auth import get_user_and_ws
from src.services.chat import handle_websocket

router = APIRouter(prefix="", tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(
    user_and_ws: Annotated[tuple[UserDTO, WebSocket] | None, Depends(get_user_and_ws)],
):
    if user_and_ws is None:
        return

    user, ws = user_and_ws

    await ws.accept()
    await handle_websocket(user, ws)
