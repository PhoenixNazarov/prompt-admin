from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.status.test_case import TestCase


class TestCaseRepository(AsyncBaseRepository[TestCase]):
    def __init__(self):
        super().__init__(TestCase)
