from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.status.test_case_info import TestCaseInfo


class TestCaseInfoRepository(AsyncBaseRepository[TestCaseInfo]):
    def __init__(self):
        super().__init__(TestCaseInfo)
