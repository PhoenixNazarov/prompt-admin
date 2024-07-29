from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.sync_data import SyncData


class SyncDataRepository(AsyncBaseRepository[SyncData]):
    def __init__(self):
        super().__init__(SyncData)
