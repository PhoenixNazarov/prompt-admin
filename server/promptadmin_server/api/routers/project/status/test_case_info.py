from fastapi import APIRouter

from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_status_service import (
    PermissionStatusService,
)

router = APIRouter()

permission_status_service = PermissionStatusService()


@router.get("/load/test_case/{id_}")
async def load_test_case(id_: int, user_data: UserDependsAnnotated):
    return await permission_status_service.load_test_case(id_, user_data)
