from dataclasses import dataclass, field
from datetime import datetime

from src.domain.exceptions import DomainException


@dataclass(kw_only=True, slots=True)
class ChatMessage:
    id: int
    sender_id: int
    recipient_id: int
    text: str
    created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, sender_id: int, recipient_id: int, text: str, created_at: datetime | None = None):
        text = text.strip()
        if len(text) > 4096:
            raise DomainException("Длина сообщения превышает 4096")

        return cls(
            id=0,
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text,
            created_at=created_at if created_at is not None else datetime.now(),
        )
