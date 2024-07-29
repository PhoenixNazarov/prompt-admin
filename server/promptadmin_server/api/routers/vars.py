from fastapi import APIRouter
from promptadmin.vars.var_service import VarService
from pydantic import BaseModel

from settings import SETTINGS

router = APIRouter()


class ProjectDto(BaseModel):
    project: str


@router.post('/load')
async def load(project_dto: ProjectDto):
    connection = SETTINGS.connections.get(project_dto.project)
    if connection is None:
        return {}
    return await VarService(connection).collect_vars()
