import contextlib

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from src.application.chat import AbstractChatManager
from src.domain.chat_message import ChatMessage
from src.domain.users import User
from src.infrastructure.db.connector import async_session_maker
from src.infrastructure.db.models import ChatMessageModel
from src.presentation.api.schemas.chat import ChatMessageSchema


class WSChatManager(AbstractChatManager):

    def __init__(self):
        self._connections: dict[int, list[WebSocket]] = {}

    async def process_message(self, msg: ChatMessage) -> None:
        # Обработка сообщения

        async with async_session_maker() as session:
            msg_model = ChatMessageModel(
                sender_id=msg.sender_id,
                recipient_id=msg.recipient_id,
                text=msg.text,
                created_at=msg.created_at,
            )
            session.add(msg_model)
            await session.commit()
            await session.refresh(msg_model)

            msg.id = msg_model.id

        await self.send_massage(msg.recipient_id, msg)  # Отправляем далее

    def add_connection(self, user_id: int, ws: WebSocket):
        if user_id not in self._connections:
            self._connections[user_id] = [ws]
        else:
            self._connections[user_id].append(ws)

    def remove_connection(self, user_id: int, ws: WebSocket):
        if user_id in self._connections:
            with contextlib.suppress(ValueError):
                self._connections[user_id].remove(ws)

            if not self._connections[user_id]:
                del self._connections[user_id]

    async def send_massage(self, user_id: int, msg: ChatMessage):
        for ws in self._connections.get(user_id, []):
            if ws:
                await ws.send_text(ChatMessageSchema.model_validate(msg).model_dump_json())
            else:
                self.remove_connection(user_id, ws)


async def handle_websocket(chat_manager: AbstractChatManager, user: User, ws: WebSocket):
    await chat_manager.add_connection(user.id, ws)

    try:
        while True:
            # Приём сообщения
            data: str = await ws.receive_text()

            # Валидация
            try:
                msg = ChatMessageSchema.model_validate_json(data)
            except ValidationError:
                continue

            await chat_manager.process_message(
                ChatMessage.create(
                    sender_id=msg.sender_id,
                    recipient_id=msg.recipient_id,
                    text=msg.text,
                    created_at=msg.created_at,
                )
            )

    except WebSocketDisconnect as exc:
        print(f"WebSocketDisconnect: {exc}")

    finally:
        if ws:
            await ws.close()

        await chat_manager.remove_connection(user.id, ws)


__chat_manager__: AbstractChatManager | None = None


def get_chat_manager() -> AbstractChatManager:
    global __chat_manager__

    if __chat_manager__ is not None:
        return __chat_manager__

    manager = WSChatManager()

    __chat_manager__ = manager
    return manager
