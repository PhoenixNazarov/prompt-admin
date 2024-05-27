import asyncio
import logging
from asyncio import Task
from typing import TypeVar, Generic, Optional, Union, Any

from sqlalchemy.sql import Select, Update

from ..entity import BaseEntity
from ..repository.async_base_repository import AsyncBaseRepository
from ..dto.view_params import ViewParams

Entity = TypeVar('Entity', bound=BaseEntity)

F = Union[str, int, bool]

logger = logging.getLogger(__name__)


class AsyncBaseService(Generic[Entity]):
    def __init__(self, repository: AsyncBaseRepository[Entity]):
        self._repository = repository

    async def find_by_id(self, _id: int) -> Optional[Entity]:
        """ find model T by id """
        return await self._repository.find_by_id(_id)

    async def find_by_ids(self, ids: list[int]) -> list[Entity]:
        """ find model T by id """
        return await self._repository.find_by_ids(ids)

    async def count_by_view_params(self, view_params: ViewParams) -> int:
        """ count, order, filter """
        return await self._repository.count_by_view_params(view_params)

    async def find_by_view_params(self, view_params: ViewParams) -> list[Entity]:
        """ find, order, filter """
        return await self._repository.find_by_view_params(view_params)

    async def find_by_view_params_first(self, view_params: ViewParams) -> Optional[Entity]:
        """ find, order, filter, first"""
        return await self._repository.find_by_view_params_first(view_params)

    async def count_by_key(self, key, val: F) -> int:
        """ count model T by keys: ? with id """
        return await self._repository.count_by_key(key, val)

    async def find_by_key(self, key, val: F) -> list[Entity]:
        """ find model T by keys: ? with id """
        return await self._repository.find_by_key(key, val)

    async def find_by_key_first(self, key, val: F) -> Optional[Entity]:
        """ find model T by keys: ? with id, first """
        return await self._repository.find_by_key_first(key, val)

    async def count_by_keys(self, key, vals: list[F]) -> int:
        """ count model T by keys: ? with ids"""
        return await self._repository.count_by_keys(key, vals)

    async def find_by_keys(self, key, vals: list[F]) -> list[Entity]:
        """ find model T by keys: ? with ids"""
        return await self._repository.find_by_keys(key, vals)

    async def find_by_keys_first(self, key, vals: list[F]) -> Optional[Entity]:
        """ find model T by keys: ? with ids, first """
        return await self._repository.find_by_keys_first(key, vals)

    async def count_all(self) -> int:
        """ count all T models"""
        return await self._repository.count_all()

    async def find_all(self) -> list[Entity]:
        """ find all T models"""
        return await self._repository.find_all()

    async def save(self, entity: Entity) -> Entity:
        """ save model """
        return await self._repository.save(entity)

    async def save_all(self, entities: list[Entity]) -> list[Entity]:
        """ save all models """
        return await self._repository.save_all(entities)

    async def remove(self, entity: Entity) -> Entity:
        """ remove model """
        return await self._repository.remove(entity)

    async def remove_all(self, entities: list[Entity]) -> list[Entity]:
        """ remove all models """
        return await self._repository.remove_all(entities)

    async def asave(self, entity: Entity) -> None:
        """ save model with not blocking"""
        asyncio.create_task(self._repository.save(entity)).add_done_callback(self.callback)

    async def asave_all(self, entities: list[Entity]) -> None:
        """ save all models with not blocking """
        asyncio.create_task(self._repository.save_all(entities)).add_done_callback(self.callback)

    async def aremove(self, entity: Entity) -> None:
        """ remove model with not blocking """
        asyncio.create_task(self._repository.remove(entity)).add_done_callback(self.callback)

    async def aremove_all(self, entities: list[Entity]) -> None:
        """ remove all models with not blocking """
        asyncio.create_task(self._repository.remove_all(entities)).add_done_callback(self.callback)

    @staticmethod
    def callback(task: Task):
        if task.exception():
            logger.error('Error when create crud async operation', exc_info=task.exception())

    async def try_get_for_update(self, _id: int) -> Optional[Entity]:
        raise NotImplementedError()

    async def find_with_sql_api_first(self, sql_api: Select) -> Optional[Entity]:
        return await self._repository.find_with_sql_api_first(sql_api)

    async def find_with_sql_api_count(self, sql_api: Select) -> Optional[Entity]:
        return await self._repository.find_with_sql_api_count(sql_api)

    async def find_with_sql_api_all(self, sql_api: Select) -> list[Entity]:
        return await self._repository.find_with_sql_api_all(sql_api)

    async def execute_sql_api(self, sql_api: Update, params: list[dict[str, Any]]) -> None:
        return await self._repository.execute_sql_api(sql_api, params)
