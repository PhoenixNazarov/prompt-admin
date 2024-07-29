from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.repository.mapping_entity_repository import MappingEntityRepository


class MappingEntityService(AsyncBaseService[MappingEntity]):
    def __init__(self, repository: MappingEntityRepository = None):
        super().__init__(repository or MappingEntityRepository())
