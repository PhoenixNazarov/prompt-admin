from promptadmin.commons.service.async_base_service import AsyncBaseService
from promptadmin.data.entity.sync_data import SyncData
from promptadmin.data.repository.sync_data_repository import SyncDataRepository


class SyncDataService(AsyncBaseService[SyncData]):
    def __init__(self, repository: SyncDataRepository = None):
        super().__init__(repository or SyncDataRepository())
