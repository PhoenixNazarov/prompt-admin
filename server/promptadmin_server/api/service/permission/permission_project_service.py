from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.sync.prompt_sync_service import PromptSyncService
from promptadmin_server.api.service.user_data import UserData
from settings import SETTINGS


class PermissionProjectService(BasePermissionService):
    def __init__(self, *args, prompt_sync_service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_sync_service = prompt_sync_service or PromptSyncService()

    async def get_projects(self, user_data: UserData):
        allow_projects = await self.access_permission_service.get_allow_projects(user_data.account)
        return list(SETTINGS.sync_edpoints.keys() & allow_projects)

    async def synchronize(self, project: str, user_data: UserData):
        await self.require_project_permission(project, 'project_synchronize', 2, user_data)
        return await self.prompt_sync_service.sync_endpoint(project)
