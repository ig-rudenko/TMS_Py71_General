from abc import ABC, abstractmethod
from typing import Self, Any


class AbstractObject(ABC):
    id: int

    @abstractmethod
    def json(self) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_data: dict) -> Self: ...


class AbstractStorage(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> AbstractObject: ...

    @abstractmethod
    def get_by(self, field: str, value: Any) -> AbstractObject: ...

    @abstractmethod
    def add(self, obj: AbstractObject): ...

    @abstractmethod
    def remove(self, id_: int) -> bool: ...
