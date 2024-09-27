from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.service.sync.prompt_sync_service import PromptSyncService
from settings import SETTINGS

router = APIRouter()

prompt_sync_service = PromptSyncService()


class ProjectDto(BaseModel):
    project: str


@router.get('/get')
async def get():
    return list(SETTINGS.sync_edpoints.keys())


@router.post('/sync')
async def sync(project_dto: ProjectDto):
    return await prompt_sync_service.sync_endpoint(project_dto.project)
