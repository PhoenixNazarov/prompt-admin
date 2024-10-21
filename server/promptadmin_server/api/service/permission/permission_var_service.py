from promptadmin.vars.var_service import VarService

from promptadmin_server.api.service.base import ConnectionMixin, BasePermissionService
from promptadmin_server.api.service.user_data import UserData


class PermissionVarService(ConnectionMixin, BasePermissionService):
    async def collect(self, project: str, user_data: UserData):
        await self.require_project_permission(
            project, "project_variables", 1, user_data
        )
        connection = self.get_connection(project)
        return await VarService(connection).collect()

    async def create(
        self, project: str, key: str, value: str, template: bool, user_data: UserData
    ):
        await self.require_project_permission(
            project, "project_variables", 2, user_data
        )
        connection = self.get_connection(project)
        return await VarService(connection).create(key, value, template)

    async def remove(self, project: str, key: str, user_data: UserData):
        await self.require_project_permission(
            project, "project_variables", 2, user_data
        )
        connection = self.get_connection(project)
        return await VarService(connection).remove(key)

    async def change(self, project: str, key: str, value: str, user_data: UserData):
        await self.require_project_permission(
            project, "project_variables", 2, user_data
        )
        connection = self.get_connection(project)
        return await VarService(connection).change(key, value)
