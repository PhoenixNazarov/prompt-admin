from typing import TypeVar, Generic, Optional, Any, Type
from sqlalchemy.sql import Select, Update

from ..dto.view_params import ViewParams, ViewParamsBuilder
from ..entity import BaseEntity
from ..sqlalchemy.sql_controller import SqlController

Entity = TypeVar('Entity', bound=BaseEntity)


class BaseRepository(Generic[Entity]):
    def __init__(self,
                 entity: Type[BaseEntity],
                 sql_controller: SqlController = None):
        sql_controller = sql_controller or SqlController()
        self._entity = entity
        module_name = self._entity.__tablename__.split('_')[0]
        self._sql_controller = sql_controller.get_by_module(module_name)
        self._block_repository = sql_controller.get_block_by_module(module_name)

    def find_by_id(self, _id: int) -> Optional[Entity]:
        """ find model T by id """
        return self._sql_controller.find_with_filter_first(self._entity, self._entity.id, _id)

    def find_by_ids(self, ids: list[int]) -> list[Entity]:
        """ find model T by id """
        return self._sql_controller.find_with_filter_all(self._entity, self._entity.id, ids)

    def count_by_view_params(self, view_params: ViewParams) -> int:
        """ count, order, filter """
        return self._sql_controller.find_by_view_params_count(self._entity, view_params)

    def find_by_view_params(self, view_params: ViewParams) -> list[Entity]:
        """ find, order, filter """
        return self._sql_controller.find_by_view_params_all(self._entity, view_params)

    def find_by_view_params_first(self, view_params: ViewParams) -> Optional[Entity]:
        """ find, order, filter, first"""
        return self._sql_controller.find_by_view_params_first(self._entity, view_params)

    def count_by_key(self, key, val) -> int:
        """ count model T by keys: ?_id with id """
        return self._sql_controller.find_with_filter_count(self._entity, key, val)

    def find_by_key(self, key, val) -> list[Entity]:
        """ find model T by keys: ? with id """
        return self._sql_controller.find_with_filter_all(self._entity, key, val)

    def find_by_key_first(self, key, val) -> Optional[Entity]:
        """ find model T by keys: ? with id, first """
        return self._sql_controller.find_with_filter_first(self._entity, key, val)

    def count_by_keys(self, key, vals: list) -> int:
        """ count model T by keys: ? with ids"""
        return self._sql_controller.find_with_filter_count(self._entity, key, vals)

    def find_by_keys(self, key, vals: list) -> list[Entity]:
        """ find model T by keys: ? with ids"""
        return self._sql_controller.find_with_filter_all(self._entity, key, vals)

    def find_by_keys_first(self, key, vals: list) -> Optional[Entity]:
        """ find model T by keys: ? with ids, first """
        return self._sql_controller.find_with_filter_first(self._entity, key, vals)

    def count_all(self) -> int:
        view_params = ViewParamsBuilder().build()
        return self._sql_controller.find_by_view_params_count(self._entity, view_params)

    def find_all(self) -> list[Entity]:
        """ find all T models"""
        view_params = ViewParamsBuilder().build()
        return self._sql_controller.find_by_view_params_all(self._entity, view_params)

    def save(self, entity: Entity) -> Entity:
        """ save model """
        return self._sql_controller.save(entity)

    def save_all(self, entities: list[Entity]) -> list[Entity]:
        """ save all models """
        return self._sql_controller.save_all(entities)

    def remove(self, entity: Entity) -> Entity:
        """ remove model """
        return self._sql_controller.remove(entity)

    def remove_all(self, entities: list[Entity]) -> list[Entity]:
        """ remove all models """
        return self._sql_controller.remove_all(entities)

    def try_get_for_update(self, _id: int) -> Entity:
        self._block_repository.try_block(self._entity.__tablename__, _id)
        return self.find_by_id(_id)

    def find_with_sql_api_first(self, sql_api: Select) -> Optional[Entity]:
        return self._sql_controller.find_with_sql_api_first(sql_api)

    def find_with_sql_api_count(self, sql_api: Select) -> Optional[Entity]:
        return self._sql_controller.find_with_sql_api_count(sql_api)

    def find_with_sql_api_all(self, sql_api: Select) -> list[Entity]:
        return self._sql_controller.find_with_sql_api_all(sql_api)

    def execute_sql_api(self, sql_api: Update, params: list[dict[str, Any]]) -> None:
        return self._sql_controller.execute(sql_api, params)
