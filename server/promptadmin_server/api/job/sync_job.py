import asyncio

from promptadmin_server.api.service.prompt_sync_service import PromptSyncService
from promptadmin_server.commons.fastapi.background_task import BackgroundTask
from settings import SETTINGS


class SyncJob(BackgroundTask):
    def __init__(self, prompt_sync_service: PromptSyncService = None):
        self.prompt_sync_service = prompt_sync_service or PromptSyncService()

    async def start(self):
        while True:
            for connection in SETTINGS.sync_edpoints.keys():
                endpoint = SETTINGS.sync_edpoints[connection]
                secret = SETTINGS.sync_secrets[connection]
                await self.prompt_sync_service.sync_endpoint(endpoint, secret)
                await asyncio.sleep(10)
            await asyncio.sleep(60 * 60 * 24)

    async def stop(self):
        pass
