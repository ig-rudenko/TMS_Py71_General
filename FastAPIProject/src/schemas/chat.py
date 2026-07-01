from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    id: int | None = None
    sender_id: int
    recipient_id: int
    text: str = Field(..., min_length=1, max_length=4096)
    created_at: datetime = Field(default_factory=datetime.now)
