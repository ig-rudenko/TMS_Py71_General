import binascii
import secrets
from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True, slots=True)
class ApiToken:
    id: int
    user_id: int
    key: str
    last_used: datetime | None = None

    @classmethod
    def create(cls, user_id: int, key_length: int = 20):
        key_length = min(max(20, key_length), 64)
        return cls(
            id=0,
            user_id=user_id,
            key=cls.generate_key(key_length),
        )

    @staticmethod
    def generate_key(length: int = 20) -> str:
        return binascii.hexlify(secrets.token_bytes(length)).decode("utf-8")
