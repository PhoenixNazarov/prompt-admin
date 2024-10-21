from typing import Any

from fastapi import APIRouter

from promptadmin_server.api.dto.project_request import ProjectRequest
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_table_service import (
    PermissionTableService,
)
from promptadmin_server.api.service.sync.client_service import ClientService

router = APIRouter()

permission_table_service = PermissionTableService()


class BaseRequest(ProjectRequest):
    url: str


class GetRequest(BaseRequest):
    pass


class PostRequest(BaseRequest):
    data: dict[str, Any] | None = None


client_service = ClientService()


@router.post("/get")
async def get(get_request: GetRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.event_get(
        get_request.project, get_request.url, user_data
    )


@router.post("/post")
async def post(post_request: PostRequest, user_data: UserDependsAnnotated):
    return await permission_table_service.event_post(
        post_request.project, post_request.url, post_request.data or {}, user_data
    )
