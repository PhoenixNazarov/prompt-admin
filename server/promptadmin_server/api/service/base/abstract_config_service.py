from abc import abstractmethod, ABC
from typing import Generic, TypeVar

from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.entity import BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)


class AbstractConfigService(Generic[Entity], ABC):
    @abstractmethod
    async def get_all(self, user_data: UserData) -> list[Entity]:
        pass

    @abstractmethod
    async def save(self, entity: Entity, user_data: UserData) -> Entity:
        pass

    @abstractmethod
    async def remove(self, id_: int, user_data: UserData) -> Entity:
        pass

    @abstractmethod
    async def find_by_key(
        self, key: str, val: str | int | bool, user_data: UserData
    ) -> list[Entity]:
        pass
