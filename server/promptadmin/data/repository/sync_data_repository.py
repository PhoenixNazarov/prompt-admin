from promptadmin.commons.repository import AsyncBaseRepository
from promptadmin.data.entity.sync_data import SyncData


class SyncDataRepository(AsyncBaseRepository[SyncData]):
    def __init__(self):
        super().__init__(SyncData)
