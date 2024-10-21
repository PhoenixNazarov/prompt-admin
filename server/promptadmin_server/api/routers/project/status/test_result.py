from fastapi import APIRouter

from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_status_service import (
    PermissionStatusService,
)

router = APIRouter()

permission_status_service = PermissionStatusService()


@router.get("/load_30/{project}")
async def load_30(project: str, user_data: UserDependsAnnotated):
    return await permission_status_service.load_30(project, user_data)


@router.get("/start/{project}")
async def start(project: str, user_data: UserDependsAnnotated):
    return await permission_status_service.start(project, user_data)
