from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.table_schema import TableSchema
from promptadmin_server.data.repository.table_schema_repository import TableSchemaRepository


class TableSchemaService(AsyncBaseService[TableSchema]):
    def __init__(self, repository: TableSchemaRepository = None):
        super().__init__(repository or TableSchemaRepository())
