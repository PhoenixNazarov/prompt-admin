from promptadmin_server.commons.repository import AsyncBaseRepository
from promptadmin_server.data.entity.unit_test import UnitTest


class UnitTestRepository(AsyncBaseRepository[UnitTest]):
    def __init__(self):
        super().__init__(UnitTest)
