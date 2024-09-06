from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.status.test_result import TestResult


class TestResultRepository(AsyncBaseRepository[TestResult]):
    def __init__(self):
        super().__init__(TestResult)
