from abc import ABC, abstractmethod

from src.domain.chat_message import ChatMessage


class AbstractChatManager(ABC):

    @abstractmethod
    async def add_connection(self, user_id: int, conn) -> None: ...

    @abstractmethod
    async def remove_connection(self, user_id: int, conn) -> None: ...

    @abstractmethod
    async def process_message(self, msg: ChatMessage) -> None: ...

    @abstractmethod
    async def send_massage(self, user_id: int, msg: ChatMessage) -> None: ...
