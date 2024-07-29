from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.commons.repository import AsyncBaseRepository


class MappingRepository(AsyncBaseRepository[Mapping]):
    def __init__(self):
        super().__init__(Mapping)
