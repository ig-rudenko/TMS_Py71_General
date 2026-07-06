from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from src.domain.users import User
from src.infrastructure.db.models import ChatMessageModel
from src.schemas.chat import ChatMessageSchema
from src.infrastructure.db.connector import async_session_maker


class WSConnectionManager:

    def __init__(self):
        self._connections: dict[int, list[WebSocket]] = {}

    def add_connection(self, user_id: int, ws: WebSocket):
        if user_id not in self._connections:
            self._connections[user_id] = [ws]
        else:
            self._connections[user_id].append(ws)

    def remove_connection(self, user_id: int, ws: WebSocket):
        if user_id in self._connections:
            try:
                self._connections[user_id].remove(ws)
            except ValueError:
                pass

            if not self._connections[user_id]:
                del self._connections[user_id]

    async def send_massage(self, user_id: int, msg: ChatMessageSchema):
        for ws in self._connections.get(user_id, []):
            if ws:
                await ws.send_text(msg.model_dump_json())
            else:
                self.remove_connection(user_id, ws)


ws_manager = WSConnectionManager()


async def handle_websocket(user: User, ws: WebSocket):
    ws_manager.add_connection(user.id, ws)

    try:
        while True:
            # Приём сообщения
            data: str = await ws.receive_text()

            # Валидация
            try:
                msg = ChatMessageSchema.model_validate_json(data)
            except ValidationError:
                continue

            await process_message(msg)

    except WebSocketDisconnect as exc:
        print(f"WebSocketDisconnect: {exc}")

    finally:
        if ws:
            await ws.close()

        ws_manager.remove_connection(user.id, ws)


async def process_message(msg: ChatMessageSchema) -> None:
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

    await ws_manager.send_massage(msg.recipient_id, msg)  # Отправляем далее
