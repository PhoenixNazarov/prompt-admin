from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.repository.mapping_repository import MappingRepository


class MappingService(AsyncBaseService[Mapping]):
    def __init__(self, repository: MappingRepository = None):
        super().__init__(repository or MappingRepository())

    async def find_by_table_field(self, table: str, field: str) -> Mapping | None:
        return await self.find_by_view_params_first(
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=Mapping.table, value=table))
            .filter(ViewParamsFilter(field=Mapping.field, value=field))
            .build()
        )
