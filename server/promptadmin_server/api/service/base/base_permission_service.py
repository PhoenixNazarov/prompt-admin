from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.access_permission_service import (
    AccessPermissionService,
)
from promptadmin_server.api.service.user_data import UserData


class BasePermissionService:
    def __init__(
        self,
        *args,
        access_permission_service: AccessPermissionService | None = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.access_permission_service = (
            access_permission_service or AccessPermissionService()
        )

    async def require_permission(self, key: str, value: int, user_data: UserData):
        if user_data.account is None:
            raise TypeCheckException()
        await self.access_permission_service.require_permission(
            key, value, user_data.account
        )

    async def require_project_permission(
        self, project: str, key: str, value: int, user_data: UserData
    ):
        if user_data.account is None:
            raise TypeCheckException()
        await self.access_permission_service.require_project_permission(
            key, project, value, user_data.account
        )
