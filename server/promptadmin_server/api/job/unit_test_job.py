import asyncio
import logging

from promptadmin_server.api.service.prompt_unit_test_service import PromptUnitTestService
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsOrder
from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.sync_data_service import SyncDataService

logger = logging.getLogger(__name__)


class UnitTestJob(BackgroundTask):
    def __init__(self,
                 sync_data_service: SyncDataService = None,
                 prompt_unit_test_service: PromptUnitTestService = None,
                 mapping_entity_service: MappingEntityService = None
                 ):
        self.sync_data_service = sync_data_service or SyncDataService()
        self.prompt_unit_test_service = prompt_unit_test_service or PromptUnitTestService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()

    async def find_by_position(self, position: int):
        view_params = ViewParamsBuilder().order(ViewParamsOrder(field=SyncData.id)).page(position).count(1).build()
        return await self.sync_data_service.find_by_view_params_first(view_params)

    async def start(self):
        await asyncio.sleep(60 * 10)
        while True:
            position = 0
            while True:
                sync_data = await self.find_by_position(position)
                if sync_data is None:
                    break
                try:
                    await self.prompt_unit_test_service.process_sync_data(sync_data, delay=5)
                except Exception as e:
                    logger.error("Exception unit testing for sync data", exc_info=e, extra={'sync_data': sync_data})
                await asyncio.sleep(5)
                position += 1

            await asyncio.sleep(60 * 10)

    async def stop(self):
        pass
