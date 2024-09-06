from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.status.test_case import TestCase
from promptadmin_server.data.repository.status.test_case_repository import TestCaseRepository


class TestCaseService(AsyncBaseService[TestCase]):
    def __init__(self, repository: TestCaseRepository = None):
        super().__init__(repository or TestCaseRepository())
