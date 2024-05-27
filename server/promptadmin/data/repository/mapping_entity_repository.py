from promptadmin.data.entity.mapping_entity import MappingEntity
from promptadmin.commons.repository import AsyncBaseRepository


class MappingEntityRepository(AsyncBaseRepository[MappingEntity]):
    def __init__(self):
        super().__init__(MappingEntity)
