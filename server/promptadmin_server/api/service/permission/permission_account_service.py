from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.access_permission_service import (
    AccessPermissionService,
)
from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.data.entity.permission import Permission
from promptadmin_server.data.service.account_service import AccountService
from settings import SETTINGS


class PermissionAccountService(BasePermissionService):
    def __init__(
        self,
        access_permission_service: AccessPermissionService | None = None,
        account_service: AccountService | None = None,
        *args,
        **kwargs
    ):
        super().__init__(
            *args, access_permission_service=access_permission_service, **kwargs
        )
        self.access_permission_service = (
            access_permission_service or AccessPermissionService()
        )
        self.account_service = account_service or AccountService()

    async def get_my_config(self, user_data: UserData) -> list[Permission]:
        if user_data.account is None:
            raise TypeCheckException()
        return await self.access_permission_service.get_config(user_data.account)

    async def get_other_config(
        self, account_id: int, user_data: UserData
    ) -> list[Permission]:
        await self.require_permission("config_accounts", 1, user_data)
        account = await self.account_service.find_by_id(account_id)
        if account is None:
            raise TypeCheckException()
        return await self.access_permission_service.get_config(account)

    async def get_projects(self, user_data: UserData) -> list[str]:
        await self.require_permission("config_accounts", 1, user_data)
        return list(SETTINGS.connections.keys() | SETTINGS.sync_edpoints.keys())

    async def set_permission(
        self,
        account_id: int,
        key: str,
        value: int,
        project: str | None,
        user_data: UserData,
    ) -> Permission:
        await self.require_permission("config_accounts", 2, user_data)
        account = await self.account_service.find_by_id(account_id)
        if account is None:
            raise TypeCheckException()
        return await self.access_permission_service.set_permission(
            account_id, key, value, project
        )
