import asyncio

from promptadmin_server.api.service.prompt_unit_test_service import PromptUnitTestService
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.service.sync_data_service import SyncDataService


class UnitTestJob(BackgroundTask):
    def __init__(self,
                 sync_data_service: SyncDataService = None,
                 prompt_unit_test_service: PromptUnitTestService = None
                 ):
        self.sync_data_service = sync_data_service or SyncDataService()
        self.prompt_unit_test_service = prompt_unit_test_service or PromptUnitTestService()

    async def start(self):
        await asyncio.sleep(60 * 10)
        while True:
            view_params = (
                ViewParamsBuilder()
                .filter(ViewParamsFilter(field=SyncData.test_status, value='wait'))
                .build()
            )
            sync_datas = await self.sync_data_service.find_by_view_params(view_params)
            for i in sync_datas:
                sync_data = await self.sync_data_service.find_by_id(i.id)
                await self.prompt_unit_test_service.process(sync_data)
                await asyncio.sleep(20)

            await asyncio.sleep(60 * 10)

    async def stop(self):
        pass
