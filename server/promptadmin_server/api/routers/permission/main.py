from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_account_service import (
    PermissionAccountService,
)
from promptadmin_server.data.entity.permission import Permission

router = APIRouter()

permission_account_service = PermissionAccountService()


class AccountRequest(BaseModel):
    account_id: int


class PermissionConfigRequest(AccountRequest):
    key: str
    value: int
    project: str | None = None


@router.get("/get")
async def get(user_data: UserDependsAnnotated) -> list[Permission]:
    return await permission_account_service.get_my_config(user_data)


@router.get("/get/projects")
async def get_projects(user_data: UserDependsAnnotated) -> list[str]:
    return await permission_account_service.get_projects(user_data)


@router.post("/get/user")
async def get_user(
    account_request: AccountRequest, user_data: UserDependsAnnotated
) -> list[Permission]:
    return await permission_account_service.get_other_config(
        account_request.account_id, user_data
    )


@router.post("/set/user")
async def set_user(
    permission_config_request: PermissionConfigRequest, user_data: UserDependsAnnotated
):
    return await permission_account_service.set_permission(
        permission_config_request.account_id,
        permission_config_request.key,
        permission_config_request.value,
        permission_config_request.project,
        user_data,
    )
