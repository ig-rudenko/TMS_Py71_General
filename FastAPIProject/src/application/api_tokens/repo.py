from abc import ABC, abstractmethod

from src.domain.api_tokens import ApiToken


class AbstractAPITokenRepository(ABC):

    @abstractmethod
    async def get_by_key(self, key: str) -> ApiToken: ...

    @abstractmethod
    async def add(self, obj: ApiToken) -> ApiToken: ...

    @abstractmethod
    async def delete(self, id_: int) -> ApiToken: ...
