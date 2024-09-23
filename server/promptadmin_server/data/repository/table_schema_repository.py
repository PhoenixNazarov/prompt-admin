from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.table_schema import TableSchema


class TableSchemaRepository(AsyncBaseRepository[TableSchema]):
    def __init__(self):
        super().__init__(TableSchema)
