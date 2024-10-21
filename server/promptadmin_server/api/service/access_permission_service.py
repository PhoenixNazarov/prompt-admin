from promptadmin_server.api.exceptions import PermissionException, TypeCheckException
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.account import Account
from promptadmin_server.data.entity.permission import Permission
from promptadmin_server.data.service.permission_service import PermissionService

__all__ = [
    "AccessPermissionService",
]

GLOBAL_DEFAULTS: dict[str, int] = {"config_tables": 1, "config_accounts": 0}

PROJECT_DEFAULTS: dict[str, int] = {
    "project_prompt": 1,
    "project_blog": 1,
    "project_variables": 1,
    "project_status": 1,
    "project_synchronize": 0,
    "project_tables_upload": 1,
    "project_tables": 1,
}


class AccessPermissionService:
    def __init__(self, permission_service: PermissionService | None = None):
        self.permission_service = permission_service or PermissionService()

    async def get_config(self):
        pass

    async def _find_permission(
        self, account_id: int, key: str, project: str | None = None
    ) -> Permission | None:
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=Permission.account_id, value=account_id))
            .filter(ViewParamsFilter(field=Permission.key, value=key))
            .filter(ViewParamsFilter(field=Permission.project, value=project))
            .build()
        )
        return await self.permission_service.find_by_view_params_first(view_params)

    async def require_permission(
        self, key: str, value: int, account: Account, raise_=True
    ) -> bool:
        if account.id is None:
            raise TypeCheckException()
        permission = await self._find_permission(account.id, key)
        result = value <= GLOBAL_DEFAULTS[key]
        if permission is not None:
            result = value <= permission.value
        if raise_ and not result:
            raise PermissionException()
        return result

    async def require_project_permission(
        self, key: str, project: str, value: int, account: Account, raise_=True
    ) -> bool:
        if account.id is None:
            raise TypeCheckException()
        project_permission = await self._find_permission(account.id, "project", project)
        if project_permission is None or (
            project_permission is not None and project_permission.value == 0
        ):
            return False

        permission = await self._find_permission(account.id, key, project)
        result = value <= PROJECT_DEFAULTS[key]
        if permission is not None:
            result = value <= permission.value
        if raise_ and not result:
            raise PermissionException()
        return result

    async def get_allow_projects(self, account: Account | None) -> list[str]:
        if account is None:
            raise TypeCheckException()
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=Permission.account_id, value=account.id))
            .filter(ViewParamsFilter(field=Permission.key, value="project"))
            .build()
        )
        permissions = await self.permission_service.find_by_view_params(view_params)

        return [p.project for p in permissions if p.project is not None and p.value > 0]
