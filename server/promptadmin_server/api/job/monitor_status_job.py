import asyncio

from promptadmin_server.api.service.sync.test_monitoring_service import TestMonitoringService
from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from settings import SETTINGS


class MonitorStatusJob(BackgroundTask):
    def __init__(
            self,
            test_monitoring_service: TestMonitoringService = None
    ):
        self.test_monitoring_service = test_monitoring_service or TestMonitoringService()

    async def start(self):
        while True:
            for connection in SETTINGS.sync_edpoints.keys():
                await self.test_monitoring_service.sync_endpoint(connection)
                await asyncio.sleep(10)
            await asyncio.sleep(60)

    async def stop(self):
        pass
