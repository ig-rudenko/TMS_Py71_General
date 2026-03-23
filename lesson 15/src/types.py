from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from .abstracts import AbstractObject


@dataclass(kw_only=True)
class User(AbstractObject):
    id: int = 0
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

    def json(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_data: dict) -> Self:
        return cls(
            id=dict_data["id"],
            username=dict_data["username"],
            first_name=dict_data["first_name"],
            last_name=dict_data["last_name"],
            email=dict_data["email"],
            password=dict_data["password"],
        )


@dataclass(kw_only=True)
class Post(AbstractObject):
    id: int = 0
    title: str
    user_id: int
    content: str
    created_at: datetime = field(default_factory=datetime.now)

    def json(self):
        return {
            **self.__dict__,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, dict_data: dict) -> Self:
        return cls(
            id=dict_data["id"],
            title=dict_data["title"],
            user_id=dict_data["user_id"],
            content=dict_data["content"],
            created_at=datetime.fromisoformat(dict_data["created_at"]),
        )
