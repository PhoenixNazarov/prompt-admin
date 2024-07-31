from fastapi import APIRouter
from promptadmin.vars.var_service import VarService
from pydantic import BaseModel

from settings import SETTINGS

router = APIRouter()


class ProjectDto(BaseModel):
    project: str


class VarKeyDto(ProjectDto):
    key: str


class VarDto(VarKeyDto):
    value: str


@router.post('/load')
async def load(project_dto: ProjectDto):
    connection = SETTINGS.connections.get(project_dto.project)
    if connection is None:
        return {}
    return [
        {
            'key': i[0],
            'value': i[1]
        }
        for i in list((await VarService(connection).collect_vars()).items())
    ]


@router.post('/create')
async def create(var_dto: VarDto):
    connection = SETTINGS.connections.get(var_dto.project)
    if connection is None:
        return {}
    return await VarService(connection).create(var_dto.key, var_dto.value)


@router.post('/remove')
async def remove(var_key_dto: VarKeyDto):
    connection = SETTINGS.connections.get(var_key_dto.project)
    if connection is None:
        return {}
    return await VarService(connection).remove(var_key_dto.key)


@router.post('/change')
async def change(var_dto: VarDto):
    connection = SETTINGS.connections.get(var_dto.project)
    if connection is None:
        return {}
    return await VarService(connection).change(var_dto.key, var_dto.value)
