import logging
from typing import TypeVar, Generic, Union

from . import AsyncBaseService
from ..entity import BaseEntity
from ..repository.async_cache_repository import AsyncCacheRepository

Entity = TypeVar('Entity', bound=BaseEntity)

F = Union[str, int, bool]

logger = logging.getLogger(__name__)


class AsyncCacheService(Generic[Entity], AsyncBaseService[Entity]):
    def __init__(self, repository: AsyncCacheRepository):
        super().__init__(repository)
