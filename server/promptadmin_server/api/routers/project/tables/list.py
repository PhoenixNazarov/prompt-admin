from fastapi import APIRouter

from promptadmin_server.api.dto.project_request import ProjectRequest
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_table_service import (
    PermissionTableService,
)
from promptadmin_server.api.service.tables.dto import (
    SortByColumn,
    FilterColumn,
    JoinColumn,
)

router = APIRouter()

permission_table_service = PermissionTableService()


class ProjectTableRequest(ProjectRequest):
    table: str


class LoadTableRequest(ProjectTableRequest):
    columns: list[str]

    count: int | None = None
    page: int | None = None
    order_by: list[SortByColumn] | None = None
    filter: list[FilterColumn] | None = None
    joins: list[JoinColumn] | None = None


@router.post("/load")
async def load(load_request: LoadTableRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.list_load(
        load_request.project,
        load_request.table,
        load_request.columns,
        load_request.count,
        load_request.page,
        load_request.order_by,
        load_request.filter,
        load_request.joins,
        user_data,
    )


@router.post("/count")
async def count(load_request: LoadTableRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.list_count(
        load_request.project,
        load_request.table,
        load_request.filter,
        load_request.joins,
        user_data,
    )


@router.post("/fetch_columns")
async def fetch_columns(
    project_request: ProjectTableRequest, user_data: UserDependsAnnotated
):
    return await permission_table_service.fetch_columns(
        project_request.project,
        project_request.table,
        user_data,
    )
