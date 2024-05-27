from typing import TypeVar, Generic, Optional, Union, Any
from sqlalchemy.sql import Select, Update

from ..repository import BaseRepository
from ..dto.view_params import ViewParams
from ..entity.base_entity import BaseEntity

Entity = TypeVar('Entity', bound=BaseEntity)

F = Union[str, int, bool]


class BaseService(Generic[Entity]):
    def __init__(self, repository: BaseRepository):
        self._repository = repository

    def find_by_id(self, _id: int) -> Optional[Entity]:
        """ find model T by id """
        return self._repository.find_by_id(_id)

    def find_by_ids(self, ids: list[int]) -> list[Entity]:
        """ find model T by id """
        return self._repository.find_by_ids(ids)

    def count_by_view_params(self, view_params: ViewParams) -> int:
        """ count, order, filter """
        return self._repository.count_by_view_params(view_params)

    def find_by_view_params(self, view_params: ViewParams) -> list[Entity]:
        """ find, order, filter """
        return self._repository.find_by_view_params(view_params)

    def find_by_view_params_first(self, view_params: ViewParams) -> Optional[Entity]:
        """ find, order, filter, first"""
        return self._repository.find_by_view_params_first(view_params)

    def count_by_key(self, key, val: F) -> int:
        """ count model T by keys: ? with id """
        return self._repository.count_by_key(key, val)

    def find_by_key(self, key, val: F) -> list[Entity]:
        """ find model T by keys: ? with id """
        return self._repository.find_by_key(key, val)

    def find_by_key_first(self, key, val: F) -> Optional[Entity]:
        """ find model T by keys: ? with id, first """
        return self._repository.find_by_key_first(key, val)

    def count_by_keys(self, key, vals: list[F]) -> int:
        """ count model T by keys: ? with ids"""
        return self._repository.count_by_keys(key, vals)

    def find_by_keys(self, key, vals: list[F]) -> list[Entity]:
        """ find model T by keys: ? with ids"""
        return self._repository.find_by_keys(key, vals)

    def find_by_keys_first(self, key, vals: list[F]) -> Optional[Entity]:
        """ find model T by keys: ? with ids, first """
        return self._repository.find_by_keys_first(key, vals)

    def count_all(self) -> int:
        """ count all T models"""
        return self._repository.count_all()

    def find_all(self) -> list[Entity]:
        """ find all T models"""
        return self._repository.find_all()

    def save(self, entity: Entity) -> Entity:
        """ save model """
        return self._repository.save(entity)

    def save_all(self, entities: list[Entity]) -> list[Entity]:
        """ save all models """
        return self._repository.save_all(entities)

    def remove(self, entity: Entity) -> Entity:
        """ remove model """
        return self._repository.remove(entity)

    def remove_all(self, entities: list[Entity]) -> list[Entity]:
        """ remove all models """
        return self._repository.remove_all(entities)

    def try_get_for_update(self, id: int) -> Optional[Entity]:
        return self._repository.try_get_for_update(id)

    def find_with_sql_api_first(self, sql_api: Select) -> Optional[Entity]:
        return self._repository.find_with_sql_api_first(sql_api)

    def find_with_sql_api_count(self, sql_api: Select) -> Optional[Entity]:
        return self._repository.find_with_sql_api_count(sql_api)

    def find_with_sql_api_all(self, sql_api: Select) -> list[Entity]:
        return self._repository.find_with_sql_api_all(sql_api)

    def execute_sql_api(self, sql_api: Update, params: list[dict[str, Any]]) -> None:
        return self._repository.execute_sql_api(sql_api, params)
