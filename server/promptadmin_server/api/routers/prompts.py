import logging

from fastapi import APIRouter
from promptadmin.types import ModelServiceInfo, Message
from pydantic import BaseModel

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.preview_template_service import PreviewTemplateService
from promptadmin_server.api.service.prompt_load_service import PromptLoadService

from settings import SETTINGS

logger = logging.getLogger(__name__)

router = APIRouter()

preview_template_service = PreviewTemplateService()
prompt_load_service = PromptLoadService()


class PreviewPromptDto(BaseModel):
    prompt: Prompt
    context: dict | None = None


class ExecutePromptDto(BaseModel):
    service_model_info: ModelServiceInfo
    history: list[Message]
    prompt: str
    parsed_model_type: dict | None = None


@router.get('/load_all')
async def load_all():
    return await prompt_load_service.load_all()


@router.post('/save')
async def save(prompt: Prompt, user_data: UserDependsAnnotated):
    return await prompt_load_service.save(prompt, user_data)


@router.post('/preview')
async def preview(preview_prompt_dto: PreviewPromptDto):
    return await preview_template_service.preview_prompt(preview_prompt_dto.prompt, preview_prompt_dto.context)


@router.post('/execute')
async def execute(execute_prompt_dto: ExecutePromptDto):
    return await preview_template_service.execute(
        execute_prompt_dto.service_model_info,
        execute_prompt_dto.prompt,
        execute_prompt_dto.history,
        execute_prompt_dto.parsed_model_type,
    )


@router.get('/connections/get_all')
async def connections_get_all():
    return list(SETTINGS.connections.keys())
