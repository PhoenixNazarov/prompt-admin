from promptadmin.data.entity.mapping import Mapping
from promptadmin.commons.repository import AsyncBaseRepository


class MappingRepository(AsyncBaseRepository[Mapping]):
    def __init__(self):
        super().__init__(Mapping)
