from typing import TypeVar, Type, Generic, Optional

from .async_base_repository import AsyncBaseRepository
from ..dto import ViewParamsBuilder, ViewParamsOrder, ViewParamsComparison
from ..dto.view_params_comparison import ComparisonType
from ..entity.order_entity import OrderEntity
from ..sqlalchemy.sql_controller import SqlController

Entity = TypeVar('Entity', bound=OrderEntity)


class AsyncOrderRepository(Generic[Entity], AsyncBaseRepository[Entity]):

    def __init__(self,
                 entity: Type[OrderEntity],
                 sql_controller: SqlController = None):
        super().__init__(entity, sql_controller)
        self._entity = entity

    async def _get_last_order(self) -> int:
        # find entity with max order
        view_params = (ViewParamsBuilder()
                       .order(ViewParamsOrder(field=self._entity.order, desc=True))
                       .build())
        last_entity = await self.find_by_view_params_first(view_params)
        if last_entity:
            return last_entity.order
        return 0

    async def save(self, entity: Entity) -> Entity:
        last_order = await self._get_last_order()
        entity.order = last_order + 1
        return await super().save(entity)

    async def save_all(self, entities: list[Entity]) -> list[Entity]:
        last_order = await self._get_last_order()
        for i in range(len(entities)):
            entities[i].order = last_order + (i + 1)
        return await super().save_all(entities)

    async def remove(self, entity: Entity):
        view_params = (ViewParamsBuilder()
                       .comparison(
            ViewParamsComparison(comparison=ComparisonType.GT, field=self._entity.order, value=entity.order))
                       .order(ViewParamsOrder(field=self._entity.order))
                       .build())
        need_move = await self.find_by_view_params(view_params)
        for i in range(len(need_move)):
            need_move[i].order = entity.order + i
        out = await super().remove(entity)
        await super().save_all(need_move)
        return out

    async def change_order(self, for_entity: Entity, after_entity: Optional[Entity] = None) -> Entity:
        """
        Move for_entity in position after_entity.
        If after_entity = None, paste in first

        For example::
            1. Simple Case:
                Before::

                    for_entity.order = 1
                    after_entity.order = 2
                After::

                    for_entity.order = 3
                    after_entity.order = 2
                    # all entities with order > 3 will be moved to order + 1

            2. None Case::
                Before::

                    for_entity.order = 10
                    after_entity = None
                After::

                    for_entity.order = 1
                    after_entity = None
                    # all entities with order >= 4 and < 10 will be moved to order + 1
        :param for_entity: Moved entity.
        :param after_entity: Entity, where need place current entity. If None, place first.
        :return: for_entity with new order
        """

        if after_entity is None and for_entity.order == 1:
            return for_entity

        view_params = ViewParamsBuilder().order(ViewParamsOrder(field=self._entity.order))

        if after_entity:
            new_order = after_entity.order + 1
            view_params.comparison(
                ViewParamsComparison(comparison=ComparisonType.GT, field=self._entity.order, value=after_entity.order))
            view_params.comparison(
                ViewParamsComparison(comparison=ComparisonType.NE, field=self._entity.order, value=for_entity.order))
            for_entity.order = new_order
        else:
            view_params.comparison(
                ViewParamsComparison(comparison=ComparisonType.LT, field=self._entity.order, value=for_entity.order))
            new_order = 1
            for_entity.order = 1

        view_params = view_params.build()
        need_move = await self.find_by_view_params(view_params)
        for i in range(len(need_move)):
            need_move[i].order = new_order + (i + 1)
        await super().save_all(need_move)
        return await super().save(for_entity)

