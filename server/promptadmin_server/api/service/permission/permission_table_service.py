from typing import Any

from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.tables.dto import (
    SortByColumn,
    FilterColumn,
    JoinColumn,
    Column,
)
from promptadmin_server.api.service.tables.table_event_service import TableEventService
from promptadmin_server.api.service.tables.table_item_service import TableItemService
from promptadmin_server.api.service.tables.table_list_service import TableListService
from promptadmin_server.api.service.user_data import UserData


class PermissionTableService(BasePermissionService):
    def __init__(
        self,
        *args,
        table_list_service: TableListService | None = None,
        table_item_service: TableItemService | None = None,
        table_event_service: TableEventService | None = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.table_list_service = table_list_service or TableListService()
        self.table_item_service = table_item_service or TableItemService()
        self.table_event_service = table_event_service or TableEventService()

    async def list_load(
        self,
        project: str,
        table: str,
        columns: list[str],
        count: int | None,
        page: int | None,
        order_by: list[SortByColumn] | None,
        filters: list[FilterColumn] | None,
        joins: list[JoinColumn] | None,
        user_data: UserData,
    ):
        await self.require_project_permission(project, "project_tables", 1, user_data)
        return await self.table_list_service.load(
            project, table, columns, count, page, order_by, filters, joins
        )

    async def list_count(
        self,
        project: str,
        table: str,
        filters: list[FilterColumn] | None,
        joins: list[JoinColumn] | None,
        user_data: UserData,
    ):
        await self.require_project_permission(project, "project_tables", 1, user_data)
        return await self.table_list_service.count(project, table, filters, joins)

    async def fetch_columns(self, project: str, table: str, user_data: UserData):
        await self.require_project_permission(project, "project_tables", 1, user_data)
        return await self.table_list_service.fetch_columns(project, table)

    async def item_load(self, project: str, table: str, id_: int, user_data: UserData):
        await self.require_project_permission(project, "project_tables", 1, user_data)
        return await self.table_item_service.load(project, table, id_)

    async def item_update(
        self,
        project: str,
        table: str,
        id_: int,
        columns: list[Column],
        user_data: UserData,
    ):
        await self.require_project_permission(project, "project_tables", 2, user_data)
        return await self.table_item_service.update(project, table, id_, columns)

    async def item_create(
        self, project: str, table: str, columns: list[Column], user_data: UserData
    ):
        await self.require_project_permission(project, "project_tables", 2, user_data)
        return await self.table_item_service.create(project, table, columns)

    async def item_delete(
        self, project: str, table: str, id_: int, user_data: UserData
    ):
        await self.require_project_permission(project, "project_tables", 2, user_data)
        return await self.table_item_service.delete(project, table, id_)

    async def event_get(self, project: str, url: str, user_data: UserData):
        await self.require_project_permission("project_tables", project, 2, user_data)
        return await self.table_event_service.get(project, url)

    async def event_post(
        self, project: str, url: str, data: dict[str, Any], user_data: UserData
    ):
        await self.require_project_permission("project_tables", project, 2, user_data)
        return await self.table_event_service.post(project, url, data)
