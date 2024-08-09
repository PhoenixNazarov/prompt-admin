from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.repository.mapping_entity_repository import MappingEntityRepository


class MappingEntityService(AsyncBaseService[MappingEntity]):
    def __init__(self, repository: MappingEntityRepository = None):
        super().__init__(repository or MappingEntityRepository())

    async def find_by_prompt_entity(
            self,
            connection_name: str,
            table: str,
            field: str,
            name: str,
            entity: str
    ) -> list[MappingEntity]:
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=MappingEntity.connection_name, value=connection_name))
            .filter(ViewParamsFilter(field=MappingEntity.table, value=table))
            .filter(ViewParamsFilter(field=MappingEntity.field, value=field))
            .filter(ViewParamsFilter(field=MappingEntity.name, value=name))
            .filter(ViewParamsFilter(field=MappingEntity.entity, value=entity))
            .build()
        )
        return await self.find_by_view_params(view_params)

    async def find_by_entity_id(self, entity: str, entity_id: int) -> list[MappingEntity]:
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=MappingEntity.entity, value=entity))
            .filter(ViewParamsFilter(field=MappingEntity.entity_id, value=entity_id))
            .build()
        )
        return await self.find_by_view_params(view_params)
