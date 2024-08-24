from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.service.prompt_sync_service import PromptSyncService
from settings import SETTINGS

router = APIRouter()

prompt_sync_service = PromptSyncService()


class ProjectDto(BaseModel):
    project: str


@router.get('/get')
async def get():
    return list(SETTINGS.connections.keys())


@router.post('/sync')
async def sync(project_dto: ProjectDto):
    endpoint = SETTINGS.sync_edpoints.get(project_dto.project)
    secret = SETTINGS.sync_secrets.get(project_dto.project)
    if endpoint and secret:
        return await prompt_sync_service.sync_endpoint(endpoint, secret)
