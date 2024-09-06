from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.status.test_result_raw import TestResultRaw
from promptadmin_server.data.repository.status.test_result_raw_repository import TestResultRawRepository


class TestResultRawService(AsyncBaseService[TestResultRaw]):
    def __init__(self, repository: TestResultRawRepository = None):
        super().__init__(repository or TestResultRawRepository())
