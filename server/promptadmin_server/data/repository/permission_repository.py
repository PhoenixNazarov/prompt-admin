from promptadmin_server.data.entity.permission import Permission
from promptadmin_server.commons.repository import AsyncBaseRepository


class PermissionRepository(AsyncBaseRepository[Permission]):
    def __init__(self):
        super().__init__(Permission)
