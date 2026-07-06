from dataclasses import dataclass
from datetime import datetime

from .exceptions import ValidationError


@dataclass(kw_only=True, slots=True)
class User:
    id: int
    username: str
    password: str
    created_at: datetime

    @classmethod
    def create(cls, *, username: str, password: str):
        username = username.strip()
        password = password.strip()
        if not username or not password:
            ValidationError("Имя пользователя и пароль обязательны")

        return cls(id=0, username=username, password=password, created_at=datetime.now())
