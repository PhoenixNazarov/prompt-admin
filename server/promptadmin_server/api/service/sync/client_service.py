import logging

import httpx

from settings import SETTINGS

logger = logging.getLogger(__name__)


class ClientService:

    @staticmethod
    async def request(connection: str, url: str):
        async with httpx.AsyncClient() as client:
            path = SETTINGS.sync_edpoints[connection]
            secret = SETTINGS.sync_secrets[connection]
            endpoint = path.removesuffix('/') + '/' + url.removeprefix('/')
            r = await client.get(endpoint, headers={'Prompt-Admin-Secret': secret})
            return r

    async def request_json(self, connection: str, url: str) -> dict:
        result = await self.request(connection, url)
        return result.json()
