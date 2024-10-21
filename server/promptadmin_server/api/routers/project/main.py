from fastapi import APIRouter

from promptadmin_server.api.dto.project_request import ProjectRequest
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_project_service import PermissionProjectService

router = APIRouter()

permission_project_service = PermissionProjectService()


@router.get('/get')
async def get(user_data: UserDependsAnnotated):
    return permission_project_service.get_projects(user_data)


@router.post('/sync')
async def sync(project_request: ProjectRequest, user_data: UserDependsAnnotated):
    return permission_project_service.synchronize(project_request.project, user_data)
