from fastapi import APIRouter

from promptadmin_server.api.dto.project_request import ProjectRequest
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.access_permission_service import AccessPermissionService
from promptadmin_server.api.service.permission.permission_var_service import PermissionVarService

router = APIRouter()

access_permission_service = AccessPermissionService()

permission_var_service = PermissionVarService()


class VarKeyDto(ProjectRequest):
    key: str


class VarDto(VarKeyDto):
    value: str


class VarCreateDto(VarDto):
    value: str
    template: bool


@router.post('/load')
async def load(project_request: ProjectRequest, user_data: UserDependsAnnotated):
    return await permission_var_service.collect(project_request.project, user_data)


@router.post('/create')
async def create(var_dto: VarCreateDto, user_data: UserDependsAnnotated):
    return await permission_var_service.create(var_dto.project, var_dto.key, var_dto.value, var_dto.template, user_data)


@router.post('/remove')
async def remove(var_key_dto: VarKeyDto, user_data: UserDependsAnnotated):
    return await permission_var_service.remove(var_key_dto.project, var_key_dto.key, user_data)


@router.post('/change')
async def change(var_dto: VarDto, user_data: UserDependsAnnotated):
    return await permission_var_service.change(var_dto.project, var_dto.key, var_dto.project, user_data)
