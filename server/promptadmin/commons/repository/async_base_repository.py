from typing import TypeVar, Generic, Optional, Any, Type
from sqlalchemy.sql import Select, Update

from ..dto.view_params import ViewParams, ViewParamsBuilder
from ..entity import BaseEntity
from ..sqlalchemy.sql_controller import SqlController

Entity = TypeVar('Entity', bound=BaseEntity)


class AsyncBaseRepository(Generic[Entity]):
    def __init__(self,
                 entity: Type[BaseEntity],
                 sql_controller: SqlController = None):
        sql_controller = sql_controller or SqlController()
        self._entity = entity
        module_name = self._entity.__tablename__.split('_')[0]
        self._sql_controller = sql_controller.get_async_by_module(module_name)

    async def find_by_id(self, _id: int) -> Optional[Entity]:
        """ find model T by id """
        return await self._sql_controller.find_with_filter_first(self._entity, self._entity.id, _id)

    async def find_by_ids(self, ids: list[int]) -> list[Entity]:
        """ find model T by id """
        return await self._sql_controller.find_with_filter_all(self._entity, self._entity.id, ids)

    async def count_by_view_params(self, view_params: ViewParams) -> int:
        """ count, order, filter """
        return await self._sql_controller.find_by_view_params_count(self._entity, view_params)

    async def find_by_view_params(self, view_params: ViewParams) -> list[Entity]:
        """ find, order, filter """
        return await self._sql_controller.find_by_view_params_all(self._entity, view_params)

    async def find_by_view_params_first(self, view_params: ViewParams) -> Optional[Entity]:
        """ find, order, filter, first"""
        return await self._sql_controller.find_by_view_params_first(self._entity, view_params)

    async def count_by_key(self, key, val) -> int:
        """ count model T by keys: ?_id with id """
        return await self._sql_controller.find_with_filter_count(self._entity, key, val)

    async def find_by_key(self, key, val) -> list[Entity]:
        """ find model T by keys: ? with id """
        return await self._sql_controller.find_with_filter_all(self._entity, key, val)

    async def find_by_key_first(self, key, val) -> Optional[Entity]:
        """ find model T by keys: ? with id, first """
        return await self._sql_controller.find_with_filter_first(self._entity, key, val)

    async def count_by_keys(self, key, vals: list) -> int:
        """ count model T by keys: ? with ids"""
        return await self._sql_controller.find_with_filter_count(self._entity, key, vals)

    async def find_by_keys(self, key, vals: list) -> list[Entity]:
        """ find model T by keys: ? with ids"""
        return await self._sql_controller.find_with_filter_all(self._entity, key, vals)

    async def find_by_keys_first(self, key, vals: list) -> Optional[Entity]:
        """ find model T by keys: ? with ids, first """
        return await self._sql_controller.find_with_filter_first(self._entity, key, vals)

    async def count_all(self) -> int:
        view_params = ViewParamsBuilder().build()
        return await self._sql_controller.find_by_view_params_count(self._entity, view_params)

    async def find_all(self) -> list[Entity]:
        """ find all T models"""
        view_params = ViewParamsBuilder().build()
        return await self._sql_controller.find_by_view_params_all(self._entity, view_params)

    async def save(self, entity: Entity) -> Entity:
        """ save model """
        return await self._sql_controller.save(entity)

    async def save_all(self, entities: list[Entity]) -> list[Entity]:
        """ save all models """
        return await self._sql_controller.save_all(entities)

    async def remove(self, entity: Entity) -> Entity:
        """ remove model """
        return await self._sql_controller.remove(entity)

    async def remove_all(self, entities: list[Entity]) -> list[Entity]:
        """ remove all models """
        return await self._sql_controller.remove_all(entities)

    async def try_get_for_update(self, _id: int) -> Entity:
        raise NotImplementedError()

    async def find_with_sql_api_first(self, sql_api: Select) -> Optional[Entity]:
        return await self._sql_controller.find_with_sql_api_first(sql_api)

    async def find_with_sql_api_count(self, sql_api: Select) -> Optional[Entity]:
        return await self._sql_controller.find_with_sql_api_count(sql_api)

    async def find_with_sql_api_all(self, sql_api: Select) -> list[Entity]:
        return await self._sql_controller.find_with_sql_api_all(sql_api)

    async def execute_sql_api(self, sql_api: Update, params: list[dict[str, Any]]) -> None:
        return await self._sql_controller.execute(sql_api, params)
