from pydantic import BaseModel
from typing import TypeVar, Generic

from .redis_pool import RedisPool
from ..entity import BaseEntity

Entity = TypeVar('Entity', bound=BaseEntity)


class RedisSettings(BaseModel):
    expiry_time: int = 100


class RedisManager(Generic[Entity]):
    def __init__(
            self,
            entity_type: type[Entity],
            redis_pool: RedisPool = None,
            redis_settings: RedisSettings = None
    ):
        self.redis_pool = redis_pool or RedisPool()
        self.redis = self.redis_pool.get_redis()
        self.entity_type = entity_type
        self.redis_settings = redis_settings or RedisSettings()

    def key_format(self, id_: int):
        return f'{self.entity_type.__tablename__}:{id_}'

    async def set(self, entity: Entity):
        if self.redis is None:
            return
        if entity.id is None:
            return
        key = self.key_format(entity.id)
        value = entity.model_dump_json()
        await self.redis.setex(key, self.redis_settings.expiry_time, value)

    async def set_all(self, entities: list[Entity]):
        if self.redis is None:
            return
        pipe = self.redis.pipeline()
        for i in entities:
            if i.id is None:
                continue
            key = self.key_format(i.id)
            value = i.model_dump_json()
            pipe.setex(key, self.redis_settings.expiry_time, value)
        await pipe.execute()

    async def get(self, id_: int) -> Entity | None:
        if self.redis is None:
            return
        key = self.key_format(id_)
        value = await self.redis.get(key)
        if value:
            return self.entity_type.model_validate_json(value)
        return None

    async def get_all(self, ids: list[int]) -> list[Entity]:
        if self.redis is None:
            return []
        keys = [self.key_format(i) for i in ids]
        values = await self.redis.mget(keys)
        return [
            self.entity_type.model_validate_json(i)
            for i in values
            if i
        ]

    async def remove(self, entity: Entity):
        if self.redis is None:
            return
        if entity.id is None:
            return
        key = self.key_format(entity.id)
        await self.redis.delete(key)

    async def remove_all(self, entities: list[Entity]):
        if self.redis is None:
            return
        keys = [
            self.key_format(i.id)
            for i in entities
            if i.id
        ]
        if len(keys) == 0:
            return
        await self.redis.delete(*keys)
