from fastapi import APIRouter

from promptadmin_server.api.dto.project_request import ProjectRequest
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_table_service import (
    PermissionTableService,
)
from promptadmin_server.api.service.tables.dto import Column

router = APIRouter()

permission_table_service = PermissionTableService()


class LoadItemRequest(ProjectRequest):
    table: str
    id: int


class SaveItemRequest(ProjectRequest):
    table: str
    columns: list[Column]


class UpdateItemRequest(ProjectRequest):
    table: str
    id: int
    columns: list[Column]


@router.post("/load")
async def load_id(load_item_request: LoadItemRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.item_load(
        load_item_request.project,
        load_item_request.table,
        load_item_request.id,
        user_data,
    )


@router.post("/update")
async def update(
    update_item_request: UpdateItemRequest, user_data: UserDependsAnnotated
):
    return await permission_table_service.item_update(
        update_item_request.project,
        update_item_request.table,
        update_item_request.id,
        update_item_request.columns,
        user_data,
    )


@router.post("/create")
async def create(save_item_request: SaveItemRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.item_create(
        save_item_request.project,
        save_item_request.table,
        save_item_request.columns,
        user_data,
    )


@router.post("/delete")
async def delete(load_item_request: LoadItemRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.item_delete(
        load_item_request.project,
        load_item_request.table,
        load_item_request.id,
        user_data,
    )
