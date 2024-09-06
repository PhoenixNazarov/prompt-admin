from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.status.test_result import TestResult
from promptadmin_server.data.repository.status.test_result_repository import TestResultRepository


class TestResultService(AsyncBaseService[TestResult]):
    def __init__(self, repository: TestResultRepository = None):
        super().__init__(repository or TestResultRepository())
