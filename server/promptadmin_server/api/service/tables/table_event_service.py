from typing import Any

from promptadmin_server.api.service.sync.client_service import ClientService


class TableEventService:
    def __init__(self, client_service: ClientService | None = None):
        self.client_service = client_service or ClientService()

    async def get(self, project: str, url: str):
        return (await self.client_service.get_request(project, url)).status_code

    async def post(self, project: str, url: str, data: dict[str, Any]):
        return (await self.client_service.post_request(project, url, data)).status_code
