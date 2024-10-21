from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.permission import Permission
from promptadmin_server.data.repository.permission_repository import (
    PermissionRepository,
)


class PermissionService(AsyncBaseService[Permission]):
    def __init__(self, repository: PermissionRepository | None = None):
        super().__init__(repository or PermissionRepository())
