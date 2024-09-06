from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.status.test_case_info import TestCaseInfo
from promptadmin_server.data.repository.status.test_case_info_repository import TestCaseInfoRepository


class TestCaseInfoService(AsyncBaseService[TestCaseInfo]):
    def __init__(self, repository: TestCaseInfoRepository = None):
        super().__init__(repository or TestCaseInfoRepository())
