from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.repository.sync_data_repository import SyncDataRepository


class SyncDataService(AsyncBaseService[SyncData]):
    def __init__(self, repository: SyncDataRepository = None):
        super().__init__(repository or SyncDataRepository())
