from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.status.test_result_raw import TestResultRaw


class TestResultRawRepository(AsyncBaseRepository[TestResultRaw]):
    def __init__(self):
        super().__init__(TestResultRaw)
