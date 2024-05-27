from typing import TypeVar, Optional, Generic

from .base_service import BaseService
from ..entity.order_entity import OrderEntity
from ..repository.order_repository import OrderRepository

Entity = TypeVar('Entity', bound=OrderEntity)


class OrderService(Generic[Entity], BaseService[Entity]):

    def __init__(self, repository: OrderRepository):
        super().__init__(repository)
        self._repository = repository

    def change_order(self, for_entity: Entity, after_entity: Optional[Entity] = None) -> Entity:
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
        return self._repository.change_order(for_entity, after_entity)
