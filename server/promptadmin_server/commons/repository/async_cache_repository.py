from typing import TypeVar, Type, Generic, Optional

from .async_base_repository import AsyncBaseRepository
from ..entity import BaseEntity
from ..redis.redis_manager import RedisManager, RedisSettings
from ..sqlalchemy.sql_controller import SqlController

Entity = TypeVar('Entity', bound=BaseEntity)


class AsyncCacheRepository(Generic[Entity], AsyncBaseRepository[Entity]):

    def __init__(
            self,
            entity: Type[BaseEntity],
            sql_controller: SqlController = None,
            redis_manager: RedisManager[Entity] = None,
            redis_settings: RedisSettings = None
    ):
        super().__init__(entity, sql_controller)
        self._entity = entity
        self.redis_manager = redis_manager or RedisManager(self._entity, redis_settings=redis_settings)

    async def save(self, entity: Entity) -> Entity:
        entity = await super().save(entity)
        await self.redis_manager.set(entity)
        return entity

    async def save_all(self, entities: list[Entity]) -> list[Entity]:
        entities = await super().save_all(entities)
        await self.redis_manager.set_all(entities)
        return entities

    async def find_by_id(self, _id: int) -> Optional[Entity]:
        entity = await self.redis_manager.get(_id)
        if entity is not None:
            return entity
        return await super().find_by_id(_id)

    async def find_by_ids(self, ids: list[int]) -> list[Entity]:
        entities = await self.redis_manager.get_all(ids)
        found_ids = [i.id for i in entities]
        need_search = [i for i in ids if i not in found_ids]
        return entities + await super().find_by_ids(need_search)

    async def remove(self, entity: Entity) -> Entity:
        await self.redis_manager.remove(entity)
        return await super().remove(entity)

    async def remove_all(self, entities: list[Entity]) -> list[Entity]:
        await self.redis_manager.remove_all(entities)
        return await super().remove_all(entities)
