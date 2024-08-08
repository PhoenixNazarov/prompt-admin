from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.unit_test import UnitTest
from promptadmin_server.data.repository.unit_test_repository import UnitTestRepository


class UnitTestService(AsyncBaseService[UnitTest]):
    def __init__(self, repository: UnitTestRepository = None):
        super().__init__(repository or UnitTestRepository())

    async def find_by_sync_data_name(self, sync_data_id: int, name: str) -> UnitTest | None:
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=UnitTest.sync_data_id, value=sync_data_id))
            .filter(ViewParamsFilter(field=UnitTest.name, value=name))
            .build()
        )
        return await self.find_by_view_params_first(view_params)
