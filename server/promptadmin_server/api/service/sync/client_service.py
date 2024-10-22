import logging
from typing import Any

import httpx

from settings import SETTINGS

logger = logging.getLogger(__name__)


class ClientService:

    @staticmethod
    async def get_request(connection: str, url: str):
        async with httpx.AsyncClient() as client:
            path = SETTINGS.sync_edpoints[connection]
            secret = SETTINGS.sync_secrets[connection]
            endpoint = path.removesuffix("/") + "/" + url.removeprefix("/")
            r = await client.get(endpoint, headers={"Prompt-Admin-Secret": secret})
            return r

    @staticmethod
    async def post_request(connection: str, url: str, data: dict[str, Any] | None):
        if data is None:
            data = {}
        async with httpx.AsyncClient() as client:
            path = SETTINGS.sync_edpoints[connection]
            secret = SETTINGS.sync_secrets[connection]
            endpoint = path.removesuffix("/") + "/" + url.removeprefix("/")
            r = await client.post(
                endpoint, headers={"Prompt-Admin-Secret": secret}, json=data
            )
            return r

    async def request_json(self, connection: str, url: str) -> dict:
        result = await self.get_request(connection, url)
        return result.json()
