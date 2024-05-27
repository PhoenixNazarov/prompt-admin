from typing import TypeVar, Optional, Generic

from .async_base_service import AsyncBaseService
from ..entity.order_entity import OrderEntity
from ..repository.async_order_repository import AsyncOrderRepository

Entity = TypeVar('Entity', bound=OrderEntity)


class AsyncOrderService(Generic[Entity], AsyncBaseService[Entity]):

    def __init__(self, repository: AsyncOrderRepository):
        super().__init__(repository)
        self._repository = repository

    async def change_order(self, for_entity: Entity, after_entity: Optional[Entity] = None) -> Entity:
        """
        Move for_entity in position after_entity.
        If after_entity = None, paste in first

        Invariant::
            for i in range(entities.sorted(lambda i: i.order):
                entities[i] = (i+1)

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
        return await self._repository.change_order(for_entity, after_entity)
